# coding: utf-8

from __future__ import unicode_literals
import json
import logging

from django.apps import apps
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView

logger = logging.getLogger('laboite.apps')

from .models import App, Boite, Tile, TileApp, PushButton
from laboite.apps.time.models import AppTime


# Boîtes

class BoiteListView(ListView):
    model = Boite

    def get_queryset(self):
        boites = Boite.objects.filter(qrcode=None)
        for boite in boites:
            boite.generate_qrcode()
            boite.save()

        boites = Boite.objects.filter(user=self.request.user)
        for boite in boites:
            tiles = Tile.objects.filter(boite=boite)
            # if this is a new tile on a new boite
            if not tiles:
                # then create a AppTime on a new tile
                tile = Tile(boite=boite)
                tile.save()
                app_time = AppTime(boite=boite, tz='Europe/Paris')
                app_time.save()
                content_type = ContentType.objects.get(app_label="laboite.apps.time", model="apptime")
                tile_app = TileApp(tile=tile, object_id=app_time.id, content_type=content_type)
                tile_app.save()
                messages.success(self.request, _(u"Une app temps a été créée sur votre boîte !"))

        return Boite.objects.filter(user=self.request.user).order_by("created_date")


def create_app_view(request, pk):
    boite = get_object_or_404(Boite, pk=pk, user=request.user)

    apps_list = []
    for model in apps.get_models():
        if issubclass(model, App):
            verbose_name =  model._meta.verbose_name.title()
            apps_list.append({'verbose_name':verbose_name[16:], 'pk':'create', 'app_label': model._meta.app_label})

    return render(request, 'boites/boite_create_app.html', {'boite': boite, 'boite_id': boite.id, 'apps': apps_list})


def tile_editor_view(request, boite_pk):
    boite = get_object_or_404(Boite, pk=boite_pk, user=request.user)

    return render(request, 'boites/tile_editor.html', {'boite': boite, 'boite_id': boite.id})


def apps_view(request, pk):
    boite = get_object_or_404(Boite, pk=pk, user=request.user)

    # update apps data
    boite.get_apps_dictionary()

    apps_list = []
    for model in apps.get_models():
        if issubclass(model, App):
            app_instances = model.objects.filter(boite=boite)
            if app_instances:
                for i, instance in enumerate(app_instances):
                    verbose_name =  model._meta.verbose_name.title()
                    app_label = model._meta.app_label
                    if app_instances.count() > 1:
                        verbose_name += ' ' + str(i + 1)
                    apps_list.append({'verbose_name':verbose_name[16:], 'pk':instance.pk, 'enabled':instance.enabled, 'app_label': model._meta.app_label, 'instance': instance})

    return render(request, 'boites/boite_apps.html', {'boite': boite, 'boite_id': boite.id, 'apps': apps_list})


def redirect_view(request, api_key):
    boite = get_object_or_404(Boite, api_key=api_key)
    return redirect('boites:update', pk=boite.pk)


def generate_api_key(request, pk):
    boite = get_object_or_404(Boite, pk=pk, user=request.user)
    boite.generate_api_key()
    boite.save()
    return redirect('boites:update', pk=pk)


class BoiteUpdateView(UpdateView):
    model = Boite
    fields = ['name', 'screen', 'sleep_time', 'wake_time']

    success_url = './'

    def get_queryset(self):
        qs = super(BoiteUpdateView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(BoiteUpdateView, self).get_context_data(**kwargs)
        context['boite'] = self.object
        context['boite_id'] = self.object.id
        context['api_key'] = Boite._meta.get_field('api_key')
        context['last_activity'] = Boite._meta.get_field('last_activity')
        context['last_connection'] = Boite._meta.get_field('last_connection')

        tiles = Tile.objects.filter(boite= self.object).order_by('id')

        if self.request.GET.get('tile') or not tiles:
            current_tile, created = Tile.objects.get_or_create(boite=self.object, pk=self.request.GET.get('tile'))
            if created and not tiles:
                content_type = ContentType.objects.get(app_label="laboite.apps.time", model="apptime")
        else:
            current_tile = tiles.first()

        previous_tile = Tile.objects.filter(boite=self.object, id__lt=current_tile.id).order_by('id').last()
        next_tile = Tile.objects.filter(boite=self.object, id__gt=current_tile.id).order_by('id').first()

        context['previous_tile'] = previous_tile
        context['current_tile'] = current_tile
        context['next_tile'] = next_tile

        return context


class BoiteDeleteView(DeleteView):
    model = Boite
    success_url = reverse_lazy('boites:list')

    def get_queryset(self):
        qs = super(BoiteDeleteView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(BoiteDeleteView, self).get_context_data(**kwargs)
        context['boite_id'] = self.object.id
        return context


class BoiteCreateView(SuccessMessageMixin, CreateView):
    model = Boite
    fields = ['name']
    template_name_suffix = '_create_form'
    success_message = _(u"%(name)s a bien été créée !")
    success_url = reverse_lazy('boites:list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(BoiteCreateView, self).form_valid(form)


class PushButtonUpdateView(UpdateView):
    model = PushButton
    fields = ['api_key']

    template_name = 'boites/pushbutton_form.html'

    def get_success_url(self):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('pk'), user=self.request.user)
        return reverse_lazy('boites:update', kwargs={'pk': boite.pk})

    def get_object(self):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('pk'), user=self.request.user)
        pb, created = PushButton.objects.get_or_create(boite=boite)
        return pb

    def get_context_data(self, **kwargs):
        context = super(PushButtonUpdateView, self).get_context_data(**kwargs)
        boite = get_object_or_404(Boite, pk=self.kwargs.get('pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('pk')

        return context

# Apps


class AppCreateView(SuccessMessageMixin, CreateView):
    template_name = 'apps/app_form.html'
    success_message = _('App a bien été créée !')

    def get_context_data(self, **kwargs):
        context = super(AppCreateView, self).get_context_data(**kwargs)
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('boite_pk')
        return context

    def get_success_url(self):
        return reverse_lazy('boites:apps', kwargs={'pk': self.kwargs.get('boite_pk')})

    def form_valid(self, form):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        form.instance.boite = boite
        form.save()
        return super(AppCreateView, self).form_valid(form)


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        return context.get(u'object').get_data()


class AppUpdateView(UpdateView, JSONResponseMixin):
    template_name = 'apps/app_form.html'

    def get_context_data(self, **kwargs):
        context = super(AppUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name[16:]
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('boite_pk')
        return context

    def get_success_url(self):
        return reverse_lazy('boites:apps', kwargs={'pk': self.kwargs.get('boite_pk')})

    def render_to_response(self, context):
        if self.request.GET.get('format') == 'json' or self.request.content_type == 'application/json':
            return self.render_to_json_response(context)
        else:
            if self.request.user.is_authenticated:
                boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
                return super(AppUpdateView, self).render_to_response(context)
            else:
                redirect('/account/login/?next=%s' % self.request.path)


class AppDeleteView(DeleteView):
    template_name = 'apps/app_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(AppDeleteView, self).get_context_data(**kwargs)
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('boite_pk')
        return context

    def get_success_url(self):
        messages.error(self.request, _('App supprimée !'))
        return reverse_lazy('boites:apps', kwargs={'pk': self.kwargs.get('boite_pk')})


class TileUpdateView(UpdateView):
    model = Tile
    template_name = 'tiles/tile_form.html'
    fields = ['transition', 'duration', 'brightness']

    def get_context_data(self, **kwargs):
        context = super(TileUpdateView, self).get_context_data(**kwargs)
        context['boite'] = self.object.boite
        context['boite_id'] = self.object.boite.id

        if self.request.GET.get('app'):
            #TODO : fix this MultipleObjectsReturned exception
            if self.request.GET.get('app') == "laboite.apps.bitmap":
                content_type = ContentType.objects.get(app_label="laboite.apps.bitmap", model="appbitmap")
            else:
                content_type = ContentType.objects.get(app_label=self.request.GET.get('app'))
            tile_app = TileApp(tile= self.object, object_id= self.request.GET.get('pk'), content_type=content_type)
            if issubclass(tile_app.content_object.__class__, App):
                tile_app.save()

        apps_list = []
        for model in apps.get_models():
            if issubclass(model, App):
                app_instances = model.objects.filter(boite=self.object.boite, enabled=True)
                if app_instances:
                    for i, instance in enumerate(app_instances):
                        verbose_name =  model._meta.verbose_name.title()
                        app_label = model._meta.app_label
                        if app_instances.count() > 1:
                            verbose_name += ' ' + str(i + 1)
                        apps_list.append({'verbose_name':verbose_name[16:], 'pk':instance.pk, 'app_label': model._meta.app_label, 'data': instance.get_data()})

        context['apps'] = apps_list

        apps_list = []
        tile_apps = TileApp.objects.filter(tile=self.object)
        for app in tile_apps:
            try:
                pk = app.pk
                verbose_name =  app.content_object._meta.verbose_name.title()
                apps_list.append({'verbose_name':verbose_name[16:], 'pk':pk, 'app_label': app.content_object._meta.app_label, 'data': app.content_object.get_data()})
            except:
                logger.exception('Tile app {} does not exist anymore'.format(app))
                app.delete()
        context['tile_apps'] = apps_list

        return context

    def get_success_url(self):
        return reverse_lazy('boites:tile', kwargs={'boite_pk': self.kwargs.get('boite_pk'), 'pk': self.kwargs.get('pk')})


class TileDeleteView(DeleteView):
    model = Tile
    template_name = 'tiles/tile_confirm_delete.html'

    def get_success_url(self):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        return reverse_lazy('boites:update', kwargs={'pk': boite.pk})

    def get_queryset(self):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        qs = super(TileDeleteView, self).get_queryset()
        return qs.filter(boite=boite)

    def get_context_data(self, **kwargs):
        context = super(TileDeleteView, self).get_context_data(**kwargs)
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context


def tileapp_view(request, boite_pk, pk):
    tile = get_object_or_404(Tile, pk=pk)

    if request.GET.get('app'):
        app = get_object_or_404(TileApp, pk=request.GET.get('app'), tile=tile)
        x = request.GET.get('x')
        y = request.GET.get('y')

        if x and y:
            app.x = x
            app.y = y
            app.save()

    return redirect('boites:tile', boite_pk= boite_pk, pk=pk)


def create_tile_view(request, boite_pk, pk):
    boite = get_object_or_404(Boite, pk=boite_pk, user=request.user)
    tile = Tile(boite=boite)
    tile.save()

    return redirect('boites:tile', boite_pk= boite_pk, pk=tile.pk)


class TileAppDeleteView(DeleteView):
    model = TileApp
    template_name = 'tiles/tileapp_confirm_delete.html'

    def get_success_url(self):
        tile = get_object_or_404(Tile, pk=self.kwargs.get('tile_pk'))
        return reverse_lazy('boites:tile', kwargs={'boite_pk': tile.boite.pk, 'pk': self.object.tile.id})

    def get_queryset(self):
        tile = get_object_or_404(Tile, pk=self.kwargs.get('tile_pk'))
        qs = super(TileAppDeleteView, self).get_queryset()
        return qs.filter(tile=tile)

    def get_context_data(self, **kwargs):
        context = super(TileAppDeleteView, self).get_context_data(**kwargs)
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

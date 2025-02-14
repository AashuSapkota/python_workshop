from django.shortcuts import render, get_object_or_404, redirect
from .models import Artists
from .forms import ArtistForm
from django.http import Http404

def artist_list(request):
    artists = Artists.objects.all()
    return render(request, 'artists/artist_list.html', {'artists': artists})


def artist_detail(request, pk):
    artist = get_object_or_404(Artists, pk=pk)
    return render(request, 'artists/artist_detail.html', {'artist': artist})


def artist_create(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artist_list')
    else:
        form = ArtistForm()
    return render(request, 'artists/artist_form.html', {'form': form})


def artist_update(request, pk):
    artist = get_object_or_404(Artists, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('artist_list')
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'artists/artist_form.html', {'form': form})


def artist_delete(request, pk):
    artist = get_object_or_404(Artists, pk=pk)
    if request.method == 'POST':
        artist.delete()
        return redirect('artist_list')
    return render(request, 'artists/artist_confirm_delete.html', {'artist': artist})


def custom_page_not_found(request, exception):
    return render(request, 'artists/404.html', status=404)


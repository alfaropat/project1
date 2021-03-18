from django.shortcuts import redirect, render

from . import util
from django import forms
from django.http import HttpResponse
import random

def redirect_index(request):
    return redirect('/wiki')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):

    if request.method == "POST":
        form = NewSearchForm(request.POST)

        if form.is_valid():
            form = form.cleaned_data["search"]

            if util.get_entry(form) != None:
                full_entry = util.get_entry(form)

                separate_entries = [entry for entry in full_entry.split("#") if entry]
                entry_info = []

                for entry in separate_entries:
                    entry_data = [entry_value.lstrip() for entry_value in entry.split("\n",2) if entry_value]
                    entry_data = [entry.rstrip() for entry in entry_data if entry]
                    entry_data[1] = [entry for entry in entry_data[1].splitlines() if entry]
                    entry_info.append(entry_data)

                return render(request, "encyclopedia/entry.html", {
                    "entry_info": entry_info
                })

            else:
                search_list = [entry for entry in util.list_entries() if form.lower() in entry.lower()]
                
                return render(request, "encyclopedia/search.html", {
                    "search_substring": form,
                    "search_list": search_list
                })
        else:
            return render(request, "encyclopedia/search.html", {
                "form": form
            })
                    
    return render(request, "encyclopedia/search.html", {
        "form": NewSearchForm()
    })

class NewSearchForm(forms.Form):
    search = forms.CharField(label="New Search")

def redirect_random(request):
    return redirect('encyclopedia:entry', name = random.choice(util.list_entries()))

def entry(request, name):

    full_entry = util.get_entry(name)

    if full_entry != None:
        separate_entries = [entry for entry in full_entry.split("#") if entry]
        entry_info = []

        for entry in separate_entries:
            entry_data = [entry_value.lstrip() for entry_value in entry.split("\n",2) if entry_value]
            entry_data = [entry.rstrip() for entry in entry_data if entry]
            entry_data[1] = [entry for entry in entry_data[1].splitlines() if entry]
            entry_info.append(entry_data)

        return render(request, "encyclopedia/entry.html", {
            "entry_info": entry_info
        })        
    
    return render(request, "encyclopedia/error.html", {
        "entry_name": name
    })
      
def add(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_name = form.cleaned_data["entry_name"]
            entry_info = form.cleaned_data["entry_info"]
            entry_content = f"# {entry_name}\n\n {entry_info}\n"

            if util.get_entry(entry_name) != None:
                return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "exists": True
                })

            util.save_entry(entry_name,entry_content)

            return redirect('encyclopedia:entry', name = entry_name)

        else:
            return render(request, "encyclopedia/add.html", {
                "form": form,
                "exists": False
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm(),
        "exists": False
    })

class NewEntryForm(forms.Form):
    entry_name = forms.CharField(label="Entry Name")
    entry_info = forms.CharField(label="Entry Info")

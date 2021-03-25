from django.shortcuts import redirect, render

from . import util
from django import forms
from django.http import HttpResponse
import random
import markdown2

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
                
                return render(request, "encyclopedia/entry.html", {
                    "entry_name": form,
                    "entry_content": markdown2.markdown(util.get_entry(form))                    
                })

            else:
                search_list = [entry for entry in util.list_entries() if form.lower() in entry.lower()]
                
                return render(request, "encyclopedia/search.html", {
                    "search_substring": form,
                    "search_list": search_list,
                    "entries_found": len(search_list)
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

        return render(request, "encyclopedia/entry.html", {
            "entry_name": name,
            "entry_content": markdown2.markdown(util.get_entry(name))
        })        
    
    return render(request, "encyclopedia/error.html", {
        "entry_name": name
    })
      
def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_name = form.cleaned_data["entry_name"]
            entry_content = form.cleaned_data["entry_info"]

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
    entry_name = forms.CharField(label="Title")
    entry_info = forms.CharField(label="Content", widget=forms.Textarea(attrs={'style':'width: 80%; height: 75%;'}))

class NewEditForm(forms.Form):
    full_entry = forms.CharField(widget=forms.Textarea(attrs={'style':'width: 80%; height: 75%;'}))

def edit(request,name):
    if request.method == "POST":
        form = NewEditForm(request.POST)

        if form.is_valid():
            entry_info = form.cleaned_data["full_entry"]
            util.save_entry(name,entry_info)

            return redirect('encyclopedia:entry', name)

        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })

    else:
        form = NewEditForm(initial={'full_entry': util.get_entry(name)})

        return render(request, "encyclopedia/edit.html", {
            "name": name,
            "form": form,
        })

from django.shortcuts import redirect, render

from . import util
from django import forms
from django.http import HttpResponse

def redirect_index(request):
    return redirect('index/')

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

                entry_names = []
                entry_infos = []

                for entry in separate_entries:
                    entry_data = [entry_value for entry_value in entry.splitlines() if entry_value]
                    entry_names.append(entry_data[0].split())
                    entry_infos.append(entry_data[1])

                return render(request, "encyclopedia/entry.html", {
                    "entry_name": entry_names,
                    "entry_info": entry_infos
                })

            else:
                search_list = any(search in entry for entry in util.list_entries())
                
                return render(request, "encyclopedia/search.html", {
                    "search_substring": search,
                    "search_list": search_list
                })
        else:
            return render(request, "tasks/search.html", {
                "form": form
            })
                    
    return render(request, "encyclopedia/search.html", {
        "form": NewSearchForm()
    })

class NewSearchForm(forms.Form):
    search = forms.CharField(label="New Search")

def entry(request, name):
    full_entry = util.get_entry(name).strip('\n')

    if full_entry != None:
        return render(request, "encyclopedia/entry.html", {
            "entry_name": name,
            "entry_info": full_entry[len(name)+2:]
        })
   
    return HttpResponse("The value is None!")


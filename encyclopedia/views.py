from django.shortcuts import redirect, render

from . import util
from django import forms
import random
import markdown2

"""
Redirects default index page to initial URL for project.
"""
def redirect_index(request):
    return redirect('/wiki')

"""
Returns the application's index page with its full list of entries.
"""
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

"""
Searches for a particual entry through a POST request.
If the entry exists in the list of entries, then the user is 
redirected to the entry page found.
If the entry is not found in the list of entries, then the user is 
taken to a resutlts page that displays all entries that contain 
the searched query as a substring.
"""
def search(request):

    if request.method == "POST":
        form = NewSearchForm(request.POST)

        if form.is_valid():
            form = form.cleaned_data["search"]

            if util.get_entry(form) != None:
                
                return redirect("encyclopedia:entry",form)

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

"""
Creates a new search form to be used in the search method.
"""
class NewSearchForm(forms.Form):
    search = forms.CharField(label="New Search")

"""
Redirects the user to a random entry page.
"""
def redirect_random(request):
    return redirect('encyclopedia:entry', name = random.choice(util.list_entries()))

"""
Checks if the entry exists in the current list of entries.
If the entry does exist, then the user is taken to the entry's 
page in the encyclopedia.
If the entry does not exist, then the user is taken to an error page.
"""
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

"""
Allows the user to create a full entry.
If the entry does not exist in the encyclopedia, then it 
will be added accordingly.
If the entry does exist, then the user will be presented 
an error on the same page.
Once the entry is successfully saved, the user is redirected 
to the new entry's page.
"""      
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

"""
Creates a new entry form to be used in the add method.
"""
class NewEntryForm(forms.Form):
    entry_name = forms.CharField(label="Title")
    entry_info = forms.CharField(label="Markdown Content", widget=forms.Textarea(attrs={'style':'width: 80%; height: 75%;'}))

"""
Allows the user to edit an existing entry's current Markdown content.
Once the entry is saved, the user is redirected to the edited entry.
"""
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

"""
Creates a new edit form to be used in the edit method.
"""
class NewEditForm(forms.Form):
    full_entry = forms.CharField(label="Markdown Content", widget=forms.Textarea(attrs={'style':'width: 80%; height: 75%;'}))

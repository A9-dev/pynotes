# How it works

pynotes [-q] action [options] 

# Actions

initdir (id), takes user through process where they have to enter an entire name for their project

add-project (ap) projectName

add-note (an) note [1], adds note to dir if initialised, else to project if specified, else to all

view (v) [2 | 3](only displays one from dir if dir is initialised, else displays all)

# Options

[--project | -p] projectName, adds note to project

[--all | -a], shows all notes even if in an initialised dir

[--project | -p] displays notes from specific project


# JSON

{

  “projectName”: {
  
    “dir”: “”, 
    
    “notes”:[“note1”,”note2”,…,“noteN”]

  },
  
  “Init-dir project”: {
  
    “dir”:”dir when ran initdir was ran”,
    
    “notes”:[“note1”,”note2”,…,“noteN”]
    
  }
  
}


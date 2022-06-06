# beautifulspoon

The project is a command line tool build upon [beautifulsoup](https://beautiful-soup-4.readthedocs.io/), or say this is a oneliner's tool for dealing with html files. With beautifulspoon, you can easily modify html files in the shell or within the scripts.

## Install

```
pip install beautifulspoon
```

## Usage

Let's prepare a test.html as below:

```
<html>
 <head>
  <title>
   Hello World
  </title>
 </head>
 <body>
  <div class="container" id="root">
   <a href="https://www.google.com">
    Google
   </a>
  </div>
 </body>
</html>
```

We can explore the functions of beautifulspoon as follow.

- Get the first HTML element matched selectors in `--select`.
```
bspoon test.html --select '#root a'
```

- `--set_name`, change the name of the selected tag.
```
$ bspoon debug/test.html --select a --set_name button|bspoon --select button
<button href="https://www.google.com">
 Google
</button>
```

- `--set_attr`, set attributes for the seleted tag.
```
$ bspoon test.html --select a --set_attr class link|bspoon --select a
<a class="link" href="https://www.google.com">
 Google
</a>
```

- `--append`, append a node(HTML) inside the selected node.
```
$ bspoon test.html --select a --append '<b>Home</b>'|bspoon --select a
<a href="https://www.google.com">
 Google
 <b>
  Home
 </b>
</a>
```

- `--extend`, extend the string(text) of the selected node. Adding `--smooth` may help _smooth_ the extended content. 
```
$ bspoon test.html --select a --extend ' It' --smooth|bspoon --select a
<a href="https://www.google.com">
 Google
    It
</a>

$ bspoon test.html --select a --extend ' It' --smooth|bspoon --select a
<a href="https://www.google.com">
 Google It
</a>
```

- `--insert`, insert a node(HTML) at the POS position inside the selected node. Arguments `--insert_before` and `--insert_after` are the same with `--insert`, with insert position specified at the first and the last slots.
```
$ bspoon test.html --select div --insert 0 '<br/>'| bspoon --select div
<div class="container" id="root">
 <br/>
 <a href="https://www.google.com">
  Google
 </a>
</div>
```

-- `--insert_before`(`--ib`), insert a node(HTML) before the selected node.
```
$ bspoon test.html --select a --insert_before '<br/>'|bspoon --select div
<div class="container" id="root">
 <br/>
 <a href="https://www.google.com">
  Google
 </a>
</div>
```
 
-- `--insert_after`(`--ia`), insert a node(HTML) next to the position of the selected node.
```
$ bspoon test.html --select a --ia '<br/>'|bspoon --select div
<div class="container" id="root">
 <a href="https://www.google.com">
  Google
 </a>
 <br/>
</div>
```

- `--clear`, clear the inner content of the seleted node.
```
$ bspoon test.html --select div --clear| bspoon --select div
<div class="container" id="root">
</div>
```

- `--decompose`, remove the node along with its inner content of the seleted node.
```
$ bspoon test.html --select div --decompose|bspoon --select body
<body>
</body>
```

- `--replace_with`, replace the seleted node with HTML.
```
$ bspoon test.html --select a --replace_with '<br/>'| bspoon --select div
<div class="container" id="root">
 <br/>
</div>
```

- `--comment`, Comment the selected node.
```
$ bspoon test.html --select a --comment|bspoon --select div
<div class="container" id="root">
 <!-- <a href="https://www.google.com">Google</a> -->
</div>
```

- `--wrap`, wrap the seleted node with tag provided(HTML).
```
$ bspoon test.html --select a --wrap '<p></p>'
| bspoon --select p
<p>
 <a href="https://www.google.com">
  Google
 </a>
</p>
```

- `--unwrap`, unwrap the selected node.
```
$ bspoon test.html --select a --unwrap|bspoon --select div
<div class="container" id="root">
 Google
</div>
```


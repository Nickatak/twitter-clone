## CSS Indentation.
All CSS classes will be indented to match their nested-level within elements. Example:

HTML:
```
<div class="style-one">
    <div class="style-two"></div>
</div>
```
Matching CSS:
```
.style-one {
    ...
}

    .style-two {
        ...
    }
```

## ClassName ordering on HTML elements.
For now, all styles will be applied with classes (even if they're only a singular element).  Classes in CSS will be ordered like so on an element:

```
<element class="native-tag lexicographical-global1 lexicographical-global2...">
```

The "native-tag" is the className on the direct-template stylesheet.  For example (Taken from `/templates/twitter/navbar/navbar_macros.html`):

```
<a class="nav-icon-container blue-background-color-hover center-content circle" href="{{ endpoint }}">
    ...
</a>
```

* `nav-icon-container` is the localized className used for the Template's specific stylesheet (`/static/twitter/navbar.css`)
* `blue-background-color-hover`, `center-content`, and `circle` are global styles and can be found in the global stylesheet (`/static/base.css`).


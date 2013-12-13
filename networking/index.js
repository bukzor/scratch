text = document.createTextNode('Javascript was here!');
body = document.getElementsByTagName('body')[0];
body.replaceChild(text, body.firstChild);

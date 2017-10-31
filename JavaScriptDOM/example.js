var paras = document.getElementsByTagName("p");
for (var i = 0; i < paras.length; i++) {
    alert(paras[i].getAttribute("title"));
}
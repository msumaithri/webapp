var req;

// Sends a new request to update the to-do list
function sendRequest() 
{
	if (window.XMLHttpRequest) 
	{
		req = new XMLHttpRequest();
	} 
	else 
	{
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	var searcharea = document.getElementById("search_area");
	var areacheck = searcharea.value;
	if(areacheck=="Neighbourhood")
	{
		req.onreadystatechange = handleResponse;
		req.open("GET", "/entrust-app/update/?id=1", true);
		req.send();
	}
	else if(areacheck=="Intracity")
	{
		req.onreadystatechange = handleResponse;
		req.open("GET", "/entrust-app/update/?id=2", true);
		req.send();
	}
	else if(areacheck=="Intercity")
	{	
		req.onreadystatechange = handleResponse;
		req.open("GET", "/entrust-app/update/?id=3", true);
		req.send();
	}

}
// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    // Removes the old to-do list items
        var list = document.getElementById("update");
        while (list.firstChild) {
                list.removeChild(list.firstChild);
                }

    // Parses the XML response to get a list of DOM nodes representing items
        var xmlData = req.responseXML;
        var items = xmlData.getElementsByTagName("tasks");
    // Adds each new todo-list item to the list
    for (var i = 0; i < items.length; ++i) {
        // Parses the item id and text from the DOM
        var taskname = items[i].getElementsByTagName("taskname")[0].textContent
        var taskdetails = items[i].getElementsByTagName("taskdetails")[0].textContent
        var id = items[i].getElementsByTagName("id")[0].textContent
        var uname = items[i].getElementsByTagName("uname")[0].textContent

	var updatebody = document.createElement("div");

	updatebody.setAttribute('class',"media");
        updatebody.style.border = "1px solid black";
	
	updatebody.innerHTML="<a href=\"#\" class=\"pull-left\"><img class=\"media-object\" src=\"/entrust-app/photo/"+uname+"\" width=\"90px\" height=\"90px\"/></a>";	
	var updatebody_inner = document.createElement("div");
	updatebody_inner.setAttribute('class',"media-body");
	updatebody_inner.innerHTML = "<h4 class=\"media-heading\">"+taskname+"</h4>"+taskdetails;
	var updatebody_moreinner = document.createElement("div");
	updatebody_moreinner.innerHTML="<a href=\"/entrust-app/accept-task/"+id+"\" class=\"pull-right\"> View full details </a>";
	updatebody_inner.appendChild(updatebody_moreinner);	
	
	updatebody.appendChild(updatebody_inner);
	list.appendChild(updatebody);
	}
}

window.setInterval(sendRequest, 10000);

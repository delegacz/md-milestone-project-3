$.ajax ({
    url: 'https://cors-anywhere.herokuapp.com/https://accounts.spotify.com/api/token',
    type: 'POST',
    data: {'grant_type':'client_credentials'},
    headers: {'Authorization':'Basic NTI2YzViNGQ0NThiNGFhOTk4ZTUwMmRjZDg4OWRjYTQ6MDg2NjUzZDgyMzJhNDFjNmI0OTkxYTg2ZDc5MjQ2ZDI='}
})
.done(function(requestedData){
    var token='Bearer ' + requestedData.access_token;
    console.log(token);
    $.ajax({
        type: 'GET',
        url: 'https://cors-anywhere.herokuapp.com/https://api.spotify.com/v1/playlists/2hU56mpHuOEAlyf64raVoG/images',
        headers: {'Authorization': token}
    }).done(function(data){
        var imageurl = JSON.parse(data);
        //var cialo = data.data[0].url;
        console.log(imageurl[0].url);

    });
});

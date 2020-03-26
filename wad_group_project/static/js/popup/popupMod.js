
//  ----------------    Source code  ---------------------------- //
// original from https://github.com/Leaflet/Leaflet/blob/master/src/layer/Popup.js
// This code is a modified version of what is located there


// Note,the update is handled serverside, where it just
// checks if the latitude and longditude are the same,
// if they are then it just updates the pin rather than
// adding a new one
function savePinUpdateToDatabase(layer){
  $.ajax({
      type: 'POST',
      beforeSend: function(request) {
      request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      url: 'WeatherSTUFF/add_pin/', // this is the view that handles the post data
      dataType: 'json',
      data: {
                'lat':layer['_latlng']['lat'],
                'lng': layer['_latlng']['lng'],
                'content': layer['_popup']['_content'] ,
                'title': layer['_popup']['_titleField']['innerText'],
                'date': '',//Date().toLocaleString(),
                'csrfmiddlewaretoken': String(csrftoken),
             },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        if(XMLHttpRequest.status == "401"){
          //User profile not authenticated
          // The changes didn't work so revert
          layer['_popup']['_content'] = layer['_popup']['_prevContent'];
          console.log(layer['_popup']['_prevTitle']);
          layer['_popup']['_title']['innerText'] = layer['_popup']['_prevTitle'];
          layer['_popup'].update();
          alert("Error "+XMLHttpRequest.status+" : "+XMLHttpRequest.responseText);
        }



      },
      //success: return true,
  });
}
// ----

// Adding nametag labels to all popup-able leaflet layers
const sourceTypes = ['Layer','Circle','CircleMarker','Marker','Polyline','Polygon','ImageOverlay','VideoOverlay','SVGOverlay','Rectangle','LayerGroup','FeatureGroup','GeoJSON']

sourceTypes.forEach( type => {
   L[type].include({
      nametag: type.toLowerCase()
   })
})

//  Adding new options to the default options of a popup
L.Popup.mergeOptions({
   removable: false,
   editable: false,
   title: "",
})

// Modifying the popup mechanics
L.Popup.include({

   // modifying the _initLayout method to include edit and remove buttons, if those options are enabled

   _initLayout: function () {
      var prefix = 'leaflet-popup',
          container = this._container = L.DomUtil.create('div',
         prefix + ' ' + (this.options.className || '') +
         ' leaflet-zoom-animated');

      var wrapper = this._wrapper = L.DomUtil.create('div', prefix + '-content-wrapper', container);

      console.log(this.options);
      if(this.options.title){
        console.log(this.options.title);
        // Add a title in bold at the top of the container
        var title = this._title = L.DomUtil.create('b', prefix + '-content', wrapper); // Change this css to look better
        title.innerHTML = this.options.title;
      }

      this._contentNode = L.DomUtil.create('div', prefix + '-content', wrapper);

      L.DomEvent.disableClickPropagation(wrapper);
      L.DomEvent.disableScrollPropagation(this._contentNode);
      L.DomEvent.on(wrapper, 'contextmenu', L.DomEvent.stopPropagation);

      this._tipContainer = L.DomUtil.create('div', prefix + '-tip-container', container);
      this._tip = L.DomUtil.create('div', prefix + '-tip', this._tipContainer);

      if (this.options.closeButton) {
         var closeButton = this._closeButton = L.DomUtil.create('a', prefix + '-close-button', container);
         closeButton.href = '#close';
         closeButton.innerHTML = '&#215;';

         L.DomEvent.on(closeButton, 'click', this._onCloseButtonClick, this);
      }

      var nametag = this.options.nametag ? this.options.nametag : this._source.nametag;

      if (this.options.removable && !this.options.editable){
         var userActionButtons = this._userActionButtons = L.DomUtil.create('div', prefix + '-useraction-buttons', wrapper);
         var removeButton = this._removeButton = L.DomUtil.create('a', prefix + '-remove-button', userActionButtons);
         removeButton.href = '#close';
         removeButton.innerHTML = `Remove this ${nametag}`;
         this.options.minWidth = 110;

         L.DomEvent.on(removeButton, 'click', this._onRemoveButtonClick, this);
      }

      if (this.options.editable && !this.options.removable){
         var userActionButtons = this._userActionButtons = L.DomUtil.create('div', prefix + '-useraction-buttons', wrapper);
         var editButton = this._editButton = L.DomUtil.create('a', prefix + '-edit-button', userActionButtons);
         editButton.href = '#edit';
         editButton.innerHTML = 'Edit';

         L.DomEvent.on(editButton, 'click', this._onEditButtonClick, this);
      }

      if (this.options.editable && this.options.removable){
         var userActionButtons = this._userActionButtons = L.DomUtil.create('div', prefix + '-useraction-buttons', wrapper);
         var removeButton = this._removeButton = L.DomUtil.create('a', prefix + '-remove-button', userActionButtons);
         removeButton.href = '#close';
         removeButton.innerHTML = `Remove this ${nametag}`;
         var editButton = this._editButton = L.DomUtil.create('a', prefix + '-edit-button', userActionButtons);
         editButton.href = '#edit';
         editButton.innerHTML = 'Edit';
         this.options.minWidth = 160;

         L.DomEvent.on(removeButton, 'click', this._onRemoveButtonClick, this);
         L.DomEvent.on(editButton, 'click', this._onEditButtonClick, this);
      }
   },

   _onRemoveButtonClick: function (e) {
      this._source.remove();
      L.DomEvent.stop(e);
   },

   _onEditButtonClick: function (e) {
      //Needs to be defined first to capture width before changes are applied
      var inputFieldWidth = this._inputFieldWidth = this._container.offsetWidth - 2*19;

      this._contentNode.style.display = "none";
      this._userActionButtons.style.display = "none";

      var wrapper = this._wrapper;
      var editScreen = this._editScreen = L.DomUtil.create('div', 'leaflet-popup-edit-screen', wrapper)

      // Added
      var titleField = this._titleField = L.DomUtil.create('div', 'leaflet-popup-input', editScreen);
      titleField.setAttribute("contenteditable", "true");
      titleField.innerHTML = this._title.innerHTML;
      //

      var inputField = this._inputField = L.DomUtil.create('div', 'leaflet-popup-input', editScreen);
      inputField.setAttribute("contenteditable", "true");
      inputField.innerHTML = this.getContent()


      //  -----------  Making the input field grow till max width ------- //
      inputField.style.width = inputFieldWidth + 'px';
      var inputFieldDiv = L.DomUtil.get(this._inputField);

      // create invisible div to measure the text width in pixels
      var ruler = L.DomUtil.create('div', 'leaflet-popup-input-ruler', editScreen);

      let thisStandIn = this;

      // Padd event listener to the textinput to trigger a check
      this._inputField.addEventListener("keydown", function(){
      // Check to see if the popup is already at its maxWidth
      // and that text doesnt take up whole field
         if (thisStandIn._container.offsetWidth < thisStandIn.options.maxWidth + 38
            && thisStandIn._inputFieldWidth + 5 < inputFieldDiv.clientWidth){
            ruler.innerHTML = inputField.innerHTML;

            if (ruler.offsetWidth + 20 > inputFieldDiv.clientWidth){
               console.log('expand now');
               inputField.style.width = thisStandIn._inputField.style.width = ruler.offsetWidth + 10 + 'px';
               thisStandIn.update();
            }
         }
      }, false)


      var inputActions = this._inputActions = L.DomUtil.create('div', 'leaflet-popup-input-actions', editScreen);
      var cancelButton = this._cancelButton = L.DomUtil.create('a', 'leaflet-popup-input-cancel', inputActions);
      cancelButton.href = '#cancel';
      cancelButton.innerHTML = 'Cancel';
      var saveButton = this._saveButton = L.DomUtil.create('a', 'leaflet-popup-input-save', inputActions);
      saveButton.href = "#save";
      saveButton.innerHTML = 'Save';

      L.DomEvent.on(cancelButton, 'click', this._onCancelButtonClick, this)
      L.DomEvent.on(saveButton, 'click', this._onSaveButtonClick, this)

      this.update();
      L.DomEvent.stop(e);
   },


   _onCancelButtonClick: function (e) {
      L.DomUtil.remove(this._editScreen);
      this._contentNode.style.display = "block";
      this._userActionButtons.style.display = "flex";

      this.update();
      L.DomEvent.stop(e);
   },

   _onSaveButtonClick: function (e) {

     // If the User is not authenticated, then may need to revert changes
     // So store them

     this._prevContent = this.getContent();
     this._prevTitle = this._title.innerText;


      var inputField = this._inputField;
      if (inputField.innerHTML.length > 0){
         this.setContent(inputField.innerHTML)
      } else {
         alert('Enter something');
      };

      // --

      var titleField = this._titleField;
      if (titleField.innerHTML.length > 0){
         this._title.innerHTML = titleField.innerHTML;
      } else {
         alert('Enter something');
      };

      L.DomUtil.remove(this._editScreen);
      this._contentNode.style.display = "block";
      this._userActionButtons.style.display = "flex";

      this.update();

      //this._source.remove(); <-- To remove the Pin

      L.DomEvent.stop(e);

      console.log(this._source)

      savePinUpdateToDatabase(this._source);


   }
})

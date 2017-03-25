/*
 * Inventory main entry point.
 *
 * js/main.js
 *
 * Variables used from HTML
 * ========================
 * IS_AUTHENTICATED -- True if already authenticated on initial page load.
 * USER_HREF -- Current user's API endpoint.
 * USERNAME -- Current user's username.
 */

"use strict";


var appConfig = {
  baseURL: location.protocol + '//' + location.host + '/api/',
  loginURL: location.protocol + '//' + location.host + '/api/accounts/login/'
};


window.App = {
  Models: {},
  Collections: {},
  Views: {},
  //Routers: {},
  models: {},
  collections: {},
  views: {},
  templates: null,
  loginModel: null,
  utils: null,
  invoiceTimeout: null,
  itemTimeout: null
};


// This function is run when logout happens, so that all data for the
// user is removed.
window.destroyApp = function() {
  App.models = {};
  App.collections = {};
  App.views = {};
  App.loginModel.clear().set(App.loginModel.defaults);
  App.invoiceTimeout = null;
  App.itemTimeout = null;
  $('div.tab-choice-pane div').not(':first').remove();
  $('div.tab-choice-pane div').empty();
};


var Utilities = function() {
  this.initialize();
};

Utilities.prototype = {

  initialize: function() {
  },

  _csrfSafeMethod: function(method) {
    // These HTTP methods do not require CSRF protection.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  },

  setHeader: function() {
    $.ajaxSetup({
      crossDomain: false,
      beforeSend: function(xhr, settings) {
        if(!this._csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
      }.bind(this)
    });
  },

  errorCB: function(jqXHR, status, errorThrown) {
    try {
      var json = $.parseJSON(jqXHR.responseText);
      var msg = '';

      for(var key in json) {
        msg += key + ": " + json[key] + "<br />";
      }

      this.showMessage(msg);
    } catch (e) {
      this.showMessage(jqXHR.statusText + ": " + jqXHR.status);
    }
  },

  showMessage: function(message, fade) {
    var $messages = $('#messages');
    $messages.html(message);
    $messages.show();

    if(fade !== (void 0) && fade === true) {
      $messages.fadeOut(7500);
    }
  },

  hideMessage: function() {
    var $messages = $('#messages');
    $messages.hide();
    $messages.empty();
  },

  mimicDjangoErrors: function(elm, data) {
    // Mimic Django error messages.
    var ul = '<ul class="errorlist"></ul>';
    var li = '<li></li>';
    var $tag = null, $errorUl = null, $errorLi = null;
    $('ul.errorlist').remove();

    for(var key in data) {
      $tag = $('select[name=' + key + '], input[name=' + key +
               '], textarea[name=' + key + ']');
      $errorUl = $(ul);

      if($tag.prev().prop('tagName') === 'LABEL') {
        $tag = $tag.prev();
        $errorUl.insertBefore($tag);
      } else if($tag.length === 0) {
        $tag = $(elm);
        $errorUl.appendTo($tag);
      }

      for(let i = 0; i < data[key].length; i++) {
        $errorLi = $(li);
        $errorLi.html(data[key][i]);
        $errorLi.appendTo($errorUl);
      }
    }
  },

  // Set a default value on an object key--similar to Python's
  // <dict>.setdefault(<key>, value).
  setDefault: function(obj, key, value) {
    if(key in obj) {
      return obj[key];
    } else {
      obj[key] = value;
      return obj[key];
    }
  },

  setLogin: function() {
    if(!IS_AUTHENTICATED) {
      var options = {
        backdrop: 'static',
        keyboard: false
      };
      new App.Views.LoginModal().show(options);
    } else {
      App.loginModel.set(
        'href', location.protocol + '//' + location.host + USER_HREF);
      this.fetchData();
    }
  },

  fetchData: function() {
    this.fetchUser();
    this.fetchRoot();
  },

  fetchUser: function() {
    if(App.models.userModel === (void 0)) {
      App.models.userModel = new App.Models.User();
    }

    return App.models.userModel.fetch({
      error: function(model, response, options) {
        App.utils.showMessage("Error: Could not get data for user '" +
                              USERNAME + "' from API.");
      }
    });
  },

  fetchRoot: function() {
    if(App.models.rootModel === (void 0)) {
      App.models.rootModel = new App.Models.RootModel();
    }

    return App.models.rootModel.fetch({
      success: function(model, response, options) {
        //console.log(model.get('projects').projects);
        App.utils.fetchProjectMeta();
        App.utils.fetchInventoryType();
        App.utils.fetchInventoryTypeMeta();
      },

      error: function(model, response, options) {
        App.utils.showMessage("Error: Could not get data from API root.");
      }
    });
  },

  fetchProjectMeta: function() {
    if(App.models.projectMeta === (void 0)) {
      App.models.projectMeta = new App.Models.ProjectMeta();
    }

    return App.models.projectMeta.fetch({
      success: function(model, response, options) {
        //console.log(model.get('projects').projects);
      },

      error: function(model, response, options) {
        App.utils.showMessage(options.textStatus + " " + options.errorThrown);
      }
    });
  },

  fetchInventoryType: function() {
    if(App.collections.inventoryType === (void 0)) {
      App.collections.inventoryType = new App.Collections.InventoryType();
    }

    return App.collections.inventoryType.fetch({
      success: function(model, response, options) {
        //console.log(model.get('projects').projects);
      },

      error: function(model, response, options) {
        App.utils.showMessage(options.textStatus + " " + options.errorThrown);
      }
    });
  },

  fetchInventoryTypeMeta: function() {
    if(App.models.inventoryTypeMeta === (void 0)) {
      App.models.inventoryTypeMeta = new App.Models.InventoryTypeMeta();
    }

    return App.models.inventoryTypeMeta.fetch({
      success: function(model, response, options) {
        //console.log(model.get('projects').projects);
      },

      error: function(model, response, options) {
        App.utils.showMessage(options.textStatus + " " + options.errorThrown);
      }
    });
  }
};

window.App.utils = new Utilities();

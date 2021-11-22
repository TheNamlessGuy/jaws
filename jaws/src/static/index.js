const Helpers = {
  isObject: function(variable) {
    return Object.prototype.toString.call(obj) === '[object Object]';
  },

  /*
   * opts: {
   *   responseType: string,
   *   onProgress: function,
   *   onFinish: function(xhr),
   *   onSuccess: function(xhr),
   * }
   */
  sendPostRequest: function(url, parameters, opts = null) {
    const data = new FormData();
    for (let key in parameters) {
      data.append(key, parameters[key]);
    }

    const xhr = new XMLHttpRequest();
    if (opts?.responseType != null) {
      xhr.responseType = opts.responseType;
    }

    if (opts?.onProgress != null) {
      xhr.upload.addEventListener('progress', opts.onProgress);
    }

    xhr.onreadystatechange = (e) => {
      if (xhr.readyState !== 4) { return; }

      if (opts?.onFinish != null) {
        opts.onFinish(xhr);
      } else if (xhr.status === 200) {
        if (opts?.onSuccess != null) {
          opts.onSuccess(xhr);
        } else {
          window.location.reload(false);
        }
      } else {
        console.error('TODO: ERROR', xhr);
      }
    };

    xhr.open('POST', url, true);
    xhr.send(data);
  },

  getCurrentUID: function() { return this.getUID(window.location.href); },
  getUID: function(url) {
    const uid = new URL(url).pathname.substr(1).split('/');
    uid.shift();
    return uid.join('/');
  },

  getCurrentPageType: function() { return this.getPageType(window.location.href); },
  getPageType: function(url) {
    return new URL(url).pathname.substr(1).split('/')[0];
  },

  redirect: function(to) {
    window.location.href = (new URL(window.location.href).origin) + to;
  },

  search: function(query = null) {
    if (query == null) {
      query = document.getElementById('search-sidebar-box-input').value;
    }

    this.redirect('/search/?q=' + query);
  },
};

window.addEventListener('load', () => {
  const searchInput = document.getElementById('search-sidebar-box-input');
  searchInput.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) { // Enter
      Helpers.search(searchInput.value);
    }
    e.stopPropagation();
  });
});

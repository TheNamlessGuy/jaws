window.addEventListener('load', () => {
  document.getElementById('submit').addEventListener('click', () => {
    const uid = Helpers.getCurrentUID();
    const title = document.getElementById('title').value.trim();
    const content = document.getElementById('content').value.trim();

    const url = '/_/' + Helpers.getCurrentPageType();
    Helpers.sendPostRequest(url, {'uid': uid, 'title': title, 'content': content}, {'onSuccess': (xhr) => {
      Helpers.redirect('/read/' + uid);
    }});
  });

  document.getElementById('move').addEventListener('click', () => {
    const uid = Helpers.getCurrentUID();
    const response = prompt('Move to which UID?', uid);
    if (response == null || response === uid) { return; }

    Helpers.sendPostRequest('/_/move', {'old': uid, 'new': response}, {'onSuccess': (xhr) => {
      Helpers.redirect('/read/' + response);
    }});
  });

  document.getElementById('delete').addEventListener('click', () => {
    const uid = Helpers.getCurrentUID();
    const response = confirm('Delete this page? UID: ' + uid);
    if (!response) { return; }

    Helpers.sendPostRequest('/_/delete', {'uid': uid}, {'onSuccess': (xhr) => {
      Helpers.redirect('/read/');
    }});
  });
});

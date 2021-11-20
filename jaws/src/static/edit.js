window.addEventListener('load', () => {
  document.getElementById('submit').addEventListener('click', () => {
    const uid = Helpers.getCurrentUID();
    const title = document.getElementById('title').value.trim();
    const content = document.getElementById('content').value.trim();

    const url = '/_/' + Helpers.getCurrentPageType();
    Helpers.sendPostRequest(url, {'uid': uid, 'title': title, 'content': content}, {'onFinish': (xhr) => {
      if (xhr.status === 200) {
        Helpers.redirect('/read/' + uid);
      } else {
        console.error('TODO: ERROR', xhr);
      }
    }});
  });
});

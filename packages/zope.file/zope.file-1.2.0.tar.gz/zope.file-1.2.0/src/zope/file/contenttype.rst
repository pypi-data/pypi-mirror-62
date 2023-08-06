====================================
 Content type and encoding controls
====================================

Files provide a view that supports controlling the MIME content type
and, where applicable, the content encoding.  Content encoding is
applicable based on the specific content type of the file.

Let's demonstrate the behavior of the form with a simple bit of
content.  We'll upload a bit of HTML as a sample document:

  >>> from io import BytesIO
  >>> sio = BytesIO(b"A <sub>little</sub> HTML."
  ...               b"  There's one 8-bit Latin-1 character: \xd8.")

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.addHeader("Authorization", "Basic mgr:mgrpw")
  >>> browser.addHeader("Accept-Language", "en-US")
  >>> browser.open("http://localhost/@@+/zope.file.File")

  >>> ctrl = browser.getControl(name="form.data")
  >>> ctrl.add_file(
  ...     sio, "text/html", "sample.html")
  >>> browser.getControl("Add").click()

We can see that the MIME handlers have marked this as HTML content:

  >>> import zope.mimetype.interfaces
  >>> import zope.mimetype.mtypes

  >>> file = getRootFolder()[u"sample.html"]
  >>> zope.mimetype.mtypes.IContentTypeTextHtml.providedBy(file)
  True

It's important to note that this also means the content is encoded
text:

  >>> zope.mimetype.interfaces.IContentTypeEncoded.providedBy(file)
  True

The "Content Type" page will show us the MIME type and encoding that
have been selected:

  >>> browser.getLink("sample.html").click()
  >>> browser.getLink("Content Type").click()

  >>> browser.getControl(name="form.mimeType").value
  ['zope.mimetype.mtypes.IContentTypeTextHtml']

The empty string value indicates that we have no encoding
information:

  >>> ctrl = browser.getControl(name="form.encoding")
  >>> print(ctrl.value)
  ['']

Let's now set the encoding value to an old favorite, Latin-1:

  >>> ctrl.value = ["iso-8859-1"]
  >>> browser.handleErrors = False
  >>> browser.getControl("Save").click()

We now see the updated value in the form, and can check the value in
the MIME content-type parameters on the object:

  >>> ctrl = browser.getControl(name="form.encoding")
  >>> print(ctrl.value)
  ['iso-8859-1']

  >>> file = getRootFolder()["sample.html"]
  >>> file.parameters
  {'charset': 'iso-8859-1'}

Something more interesting is that we can now use a non-encoded
content type, and the encoding field will be removed from the form:

  >>> ctrl = browser.getControl(name="form.mimeType")
  >>> ctrl.value = ["zope.mimetype.mtypes.IContentTypeImageTiff"]
  >>> browser.getControl("Save").click()

  >>> browser.getControl(name="form.encoding")
  Traceback (most recent call last):
    ...
  LookupError: name 'form.encoding'
  ...

If we switch back to an encoded type, we see that our encoding wasn't
lost:

  >>> ctrl = browser.getControl(name="form.mimeType")
  >>> ctrl.value = ["zope.mimetype.mtypes.IContentTypeTextHtml"]
  >>> browser.getControl("Save").click()

  >>> browser.getControl(name="form.encoding").value
  ['iso-8859-1']

On the other hand, if we try setting the encoding to something which
simply cannot decode the input data, we get an error message saying
that's not going to work, and no changes are saved:

  >>> ctrl = browser.getControl(name="form.encoding")
  >>> ctrl.value = ["utf-8"]

  >>> browser.getControl("Save").click()

  >>> print(browser.contents)
  <...Selected encoding cannot decode document...

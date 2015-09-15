from splinter.browser import Browser

def before_all(context):
    browser = context.config.userdata.get('browser')
    if browser is not None:
        context.browser = Browser(browser)
    else:
        context.browser = Browser('firefox')
    context.base_url = context.config.userdata.get("base_url")
    context.admin_username = context.config.userdata.get("username")
    context.admin_password = context.config.userdata.get("password")

def after_all(context):
    context.browser.quit()
    context.browser = None

def after_step(context, step):
    if step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)

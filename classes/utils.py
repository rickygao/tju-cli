def show_and_input(prompt):
    def callback(captcha_image):
        captcha_image.show()
        captcha = input(prompt)
        return captcha if captcha != '' else None
    return callback

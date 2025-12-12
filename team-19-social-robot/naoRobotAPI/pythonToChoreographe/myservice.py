import qi

#http://doc.aldebaran.com/2-8/dev/tutos/create_a_new_service.html
# import helper
# import mylib

class MyService:

    def echo(self, message):
        return message

    def do_something(self):
        pass


def main():
    app = qi.Application()
    app.start()
    session = app.session
    myService = MyService()
    session.registerService("MyService", myService)
    app.run()


if __name__ == "__main__":
    main()

import dotenv
import os
import tornado.ioloop

dotenv.load_dotenv(os.path.dirname(os.path.realpath(__file__)) + "/.env")

from energy_gauntlet.app import application

if __name__ == "__main__":
  application.listen(os.environ.get('PORT', 8888))
  tornado.ioloop.IOLoop.instance().start()

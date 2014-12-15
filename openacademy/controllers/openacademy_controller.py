from openerp import http
from openerp.http import request

class website_controller(http.Controller):

	@http.route("/hello/world", auth="public")
	def test1(self):
		return "Hello World"

	@http.route("/hello/world1", auth="public")
	def test(self):
		return "<b>Hello World</b>"

	@http.route("/hello/world_login", auth="user")
	def test_login(self):
		return "<b>Hello %s</b>"% request.env.user.name


#webpage 

	@http.route("/simple_page", auth="public", website=True)
	def simple_page(self):
		return http.request.render("openacademy.simple_page", {})

	@http.route("/dynamic_page", auth="user", website=True)
	def dynamic_page(self):
		return http.request.render("openacademy.dynamic_page", {'user': request.env.user})

	@http.route("/openacademy/course", auth="public", website=True)
	def openacademy_course(self):
		courses = request.env['openacademy.course'].search([])
		return http.request.render("openacademy.openacademy_course", {'courses': courses})

	@http.route("/openacademy/course/<model('openacademy.course'):course>", auth="public", website=True)
	def openacademy_course_details(self, course):
		return http.request.render("openacademy.openacademy_course_details", {'course': course})

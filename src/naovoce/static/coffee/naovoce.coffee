@Naovoce = {} # Application namespace


class JsonStorage
	###
	Provides getting and setting JSON-serialized objects in localStorage,
	which otherwise supports key-value strings storage only.
	###
	constructor: (namespace) ->
		if Storage?
			storage = localStorage

			@getObject = (name) ->
				data = storage.getItem(namespace)
				if data then JSON.parse(data)[name] else null

			@setObject = (name, val) ->
				data = storage.getItem(namespace)
				data = if data then JSON.parse(data) else {}
				data[name] = val
				storage.setItem namespace, JSON.stringify data

		else
			@getObject = @setObject = -> null


@Naovoce.storage = new JsonStorage('naovoce')


# Enhance strings with truncete method.
String::truncate = (n) ->
	@substr(0, n - 1).trim() + ((if @length > n then "&hellip;" else ""))


$.fn.fillViewport = ->
	###
	jQuery plugin for stretching an element height to fill down the browser window
	###
	$window = $(window)
	$elem = this
	navigation_h = $('#main-nav').outerHeight() + $('#user-info').outerHeight()

	$window.resize ->
		$elem.css 'min-height', "#{ Math.max $window.height() - navigation_h, 320 }px"
	.trigger 'resize'


$('#main-content').fillViewport()

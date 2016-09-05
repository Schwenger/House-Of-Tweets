#=require <connector.coffee>
#=require <model.coffee>
#=require <global.coffee>

citizenBirdMQ = undefined
citizenBirdSelection = undefined
dropdownTrigger = undefined
dropdownList = undefined

# this is optional to close the list while the new page is loading
# list.click(function() {
#     trigger.click();
# });

prepareCitizenBirdsPage = ->
	# attach handler to save button
	citizenBirdMQ = openConnection(global.rabbitMQ.citizenUserQueue, undefined)
	vivifyCitizenBirdsList()
	$('#submit-citizen-bird').click(submit_citizen_bird)
	dropdownTrigger = $('#bird-dropdown-button')
	dropdownList = $('#bird-dropdown-list')

	dropdownTrigger.click toggleDropdown

	$("submit-citizen-bird").click submit_citizen_bird
	resetDropdownTrigger()

resetCitizenBird = ->
	resetDropdownTrigger()
	closeDropdown()
	$('#citizen-user-name-input').val("")

resetDropdownTrigger = ->
	for own id, bird of Model.birds
		citizenBirdSelection = id
		dropdownTrigger?.text(bird[util.addLang "name"])
		break
	
toggleDropdown = ->
	dropdownTrigger.toggleClass('active')
	dropdownList.slideToggle(200)

closeDropdown = ->
	toggleDropdown() if dropdownTrigger.hasClass('active')

selectCitizenBirdFactory = (id) ->
	() ->
		citizenBirdSelection = id
		dropdownTrigger.text(Model.birds[id][util.addLang("name")])
		toggleDropdown()

vivifyCitizenBirdsList = ->
	list = $('#bird-dropdown-list')
	for own id, bird of Model.birds 
		option_object = $("<li class='bird-dropdown-entry' value=#{id}>")
		option_object.text(bird[util.addLang "name"])
		list.append(option_object)
		option_object.click selectCitizenBirdFactory(id)
		
submit_citizen_bird = (event) ->
	event.preventDefault()
	username = $('#citizen-user-name-input').val()
	data = {twittername:username, birdid:citizenBirdSelection}
	sendToQueue(citizenBirdMQ, data)
	resetCitizenBird()
	$("#carousel-control-prev").click()

translateCitizenBirds = ->
	dropdownList?.children().each(() -> $(this).remove())
	list = $('#bird-dropdown-list')
	for own id, bird of Model.birds 
		option_object = $("<li class='bird-dropdown-entry' value=#{id}>")
		option_object.text(bird[util.addLang "name"])
		list.append(option_object)
		option_object.click selectCitizenBirdFactory(id)
	resetDropdownTrigger()

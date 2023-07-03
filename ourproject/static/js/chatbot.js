
  
function talk() {
  var know = {
    "hello": ["Hello! How can I assist you today?", "Hello! How can I help you?"],
    "how are you": ["Good :)", "Fine! What about you?"],
    "what is online courier management": ["Online courier management is a system for managing courier packages through an online platform."],
    "what are the benefits of online courier management": ["Benefits include convenience, package tracking, streamlined scheduling, automated processes, improved communication, cost savings, and reduced paperwork."],
    "how does online courier management work": ["Users register, create packages, schedule pickups, track packages, and confirm deliveries through the online platform."],
    "what features are included in online courier management systems": ["Features typically include package tracking, pickup and delivery scheduling, address validation, shipping label generation, notifications, payment processing, reporting, and customer support."],
    "how can I track my package using online courier management": ["Enter the tracking number provided by the courier service into the platform to view real-time package status and location."],
    "can I schedule a pickup for my package through online courier management": ["Yes, online courier management systems allow you to schedule pickups at your preferred date and time."],
    "what if my package gets lost or damaged during transit": ["Contact customer support through the online platform to resolve the issue and file a claim if necessary."],
    "are there restrictions on package size or weight": ["Yes, there may be maximum size and weight limits for packages. Check with the courier service provider for specific guidelines."],
    "can I use online courier management for international shipments": ["Yes, online courier management systems often support international shipments with additional features for customs documentation and tracking."],
    "is online payment available for shipping fees": ["Yes, many platforms integrate with payment gateways for secure online payments of shipping fees."]
  };
  

  var user = document.getElementById('userBox').value;
  document.getElementById('chatLog').innerHTML = user + "<br>";
  let text = user.toLowerCase();
  
  if (text in know) {
    var responses = know[text];
    var randomIndex = Math.floor(Math.random() * responses.length);
    var response = responses[randomIndex];
    document.getElementById('chatLog').innerHTML = response + "<br>";
  } 
  else 
  {
    document.getElementById('chatLog').innerHTML = "Sorry, I didn't understand.<br>";
  }
}




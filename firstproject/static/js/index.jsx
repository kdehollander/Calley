//var Hello = React.createClass({
//  render: function() {
//    return <div>Hello {this.props.name}</div>;
//  }
//});

ReactDOM.render(
  <h1>Hello World</h1>,
  document.getElementById('event_list')
);
ReactDOM.render(
  Group.objects.all(),
  document.getElementById('group_list')
);

var update = setInterval(function(){
  ReactDOM.render(
    <ExampleApplication/>,
    document.getElementById('event_list')
  )
}, 500);
var update = setInterval(function(){
  ReactDOM.render(
    <ExampleApplication/>,
    document.getElementById('group_list')
  )
}, 500);

/* var start = new Date().getTime();
var ExampleApplication = React.createClass({
  render: function(){
      var current = new Date().getTime();
      return <p>Time elapsed: {current-start}</p>;
  }
});

var update = setInterval(function(){
  ReactDOM.render(
    <ExampleApplication/>,
    document.getElementById('suggest_list')
  )
}, 500);*/

/*
var ExampleApplication = React.createClass({
  render: function(){
    var listItems = this.props.data.events.map(function(item){
      return(
        <li key={item.name}>{item.time}</li>
      )
    });
    return <ul>{listItems}</ul>
  }
});

var ExampleApplicationFactory =
    React.createFactory(ExampleApplication);

var update = setInterval(function(){
  $.ajax({
    url: "/events",
    success: function(data){
      ReactDOM.render(
        ExampleApplicationFactory({data: data}),
        document.getElementById('event_list')
      );
    }
  })
}, 500);
*/

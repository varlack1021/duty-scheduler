(this["webpackJsonpmy-app"]=this["webpackJsonpmy-app"]||[]).push([[0],{21:function(e,a,t){e.exports=t(33)},26:function(e,a,t){},28:function(e,a,t){},33:function(e,a,t){"use strict";t.r(a);var n=t(0),r=t.n(n),c=t(18),l=t.n(c),o=(t(26),t(6)),u=t(12),m=t(14),s=t.n(m),i=t(19),p=t(15),d=(t(28),t(29),t(9)),f=t(5),b=t(7),E=t(20);var h=function(){var e=Object(n.useState)({hall:"",startDate:"",endDate:"",doubleDuty:!1}),a=Object(p.a)(e,2),t=a[0],c=a[1],l=Object(n.useState)([{name:"",preferences:[""],SRA:!1}]),m=Object(p.a)(l,2),h=m[0],y=m[1],v=function(){var e=Object(i.a)(s.a.mark((function e(a){var n,r,c,l;return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a.preventDefault(),console.log(t),t.staffData=h,n={method:"POST","Content-Type":"application/json",body:JSON.stringify(t),responseType:"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},e.next=6,fetch("http://localhost:8000/schedule_duty",n);case 6:return r=e.sent,c=document.createElement("a"),e.t0=URL,e.next=11,r.blob();case 11:e.t1=e.sent,l=e.t0.createObjectURL.call(e.t0,e.t1),c.download="Duty Calendar",c.href=l,document.body.appendChild(c),c.click(),document.body.removeChild(c);case 18:case"end":return e.stop()}}),e)})));return function(a){return e.apply(this,arguments)}}();return r.a.createElement("div",{className:"App"},r.a.createElement("p",{className:"Seperation"},"This text is to have a component between the first component I want padding and the top"),r.a.createElement("h1",{className:"App-header"}," Residence Life Auto Duty Scheduler "),r.a.createElement(E.a,{className:"Form-Format"},r.a.createElement(f.a,{onSubmit:function(e){return v(e)}},r.a.createElement(f.a.Label,{className:"Scheduling-options",style:{marginBottom:"20px"}},"Duty Scheduling Options"),r.a.createElement(f.a.Row,null,r.a.createElement(f.a.Group,null,r.a.createElement(f.a.Label,null,"Start Date"),r.a.createElement(f.a.Control,{type:"date",required:"True",onChange:function(e){return c(Object(o.a)(Object(o.a)({},t),{},{startDate:e.target.value}))}})),r.a.createElement(f.a.Group,null,r.a.createElement(b.a,{xs:"auto"},r.a.createElement(f.a.Label,null,"End Date"),r.a.createElement(f.a.Control,{required:"True",type:"date",onChange:function(e){return c(Object(o.a)(Object(o.a)({},t),{},{endDate:e.target.value}))}})))),r.a.createElement(f.a.Row,null,r.a.createElement(f.a.Group,{className:"input-box"},r.a.createElement(f.a.Control,{type:"text",placeholder:"Enter Hall Name",onChange:function(e){return c(Object(o.a)(Object(o.a)({},t),{},{hall:e.target.value}))},value:t.hall})),r.a.createElement(f.a.Group,null,r.a.createElement(b.a,{xs:"auto"},r.a.createElement(f.a.Check,{type:"checkBox",label:"Weekend Double Duty",className:"doubleDuty-checkBox",onClick:function(){return c(Object(o.a)(Object(o.a)({},t),{},{doubleDuty:!t.doubleDuty}))}})))),r.a.createElement(f.a.Label,{className:"Staff-members",style:{marginBottom:"15px"}},"Staff Members "),h.map((function(e,a){return r.a.createElement(r.a.Fragment,null,r.a.createElement(f.a.Row,null,r.a.createElement(f.a.Group,{key:a,className:"input-box"},r.a.createElement(f.a.Label,null," Name "),r.a.createElement(f.a.Control,{type:"text",required:"True",placeholder:"Enter staff member",onChange:function(e){return y(h.map((function(t,n){return a===n?Object(o.a)(Object(o.a)({},h[a]),{},{name:e.target.value}):t})))},value:h[a].name})),r.a.createElement(f.a.Group,{className:"sra-checkbox"},r.a.createElement(b.a,{xs:"auto"},r.a.createElement(f.a.Check,{type:"checkBox",label:"SRA",className:"sra-checkBox",onClick:function(){return y(h.map((function(e,t){return a===t?Object(o.a)(Object(o.a)({},h[a]),{},{SRA:!0}):e})))}})))),r.a.createElement(f.a.Label,null,"Days Cannot Sit"),r.a.createElement(f.a.Row,null,h[a].preferences.map((function(e,t){return r.a.createElement(r.a.Fragment,null,r.a.createElement(b.a,{xs:"auto"},r.a.createElement(f.a.Group,{key:a},r.a.createElement(f.a.Control,{type:"date",onChange:function(e){return y(h.map((function(n,r){return a===r?Object(o.a)(Object(o.a)({},h[a]),{},{preferences:n.preferences.map((function(a,n){return t===n?e.target.value:a}))}):n})))},value:h[a].preferences[t]}))))})),r.a.createElement(b.a,null,r.a.createElement(d.a,{variant:"secondary",className:"btn.btn-secondary",onClick:function(){return function(e){console.log(t),h[e.index].preferences.push(""),y(Object(u.a)(h))}({index:a})}},"Add date"))),r.a.createElement(f.a.Row,null,r.a.createElement(b.a,null,r.a.createElement(d.a,{variant:"danger",onClick:function(){return function(e){h.splice(e.index,1),y(Object(u.a)(h))}({index:a})},style:{marginBottom:"35px"}},"Remove Staff Member"))))})),r.a.createElement(f.a.Row,{className:"submit-row"},r.a.createElement(f.a.Group,null,r.a.createElement(d.a,{variant:"primary",type:"submit"},"Submit")),r.a.createElement(f.a.Group,null,r.a.createElement(b.a,null,r.a.createElement(d.a,{variant:"secondary",onClick:function(){y([].concat(Object(u.a)(h),[{name:"",preferences:[""]}]))}},"Add staff member")))))),r.a.createElement("footer",{className:"Footer"}," \xa9 Pharez J. Varlack "))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));l.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(h,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[21,1,2]]]);
//# sourceMappingURL=main.f81b22c2.chunk.js.map
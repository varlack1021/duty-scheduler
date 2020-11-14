import React, { Fragment, useState } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import AppendForm from "./appendForm";
import Card from "react-bootstrap/Card";
import Dropdown from "react-bootstrap/Dropdown";

function App() {
  let [formData, setFormData] = useState({
    hall: "",
    startDate: "",
    endDate: "",
  });

  let [staffData, setStaffData] = useState([
    {
      name: "",
      preferences: [""],
    },
  ]);

  const sendFormData = async (formEvent) => {
    formEvent.preventDefault();
    console.log(formData);
    formData.staffData = staffData;
    const requestOptions = {
      method: "POST",
      'Content-Type': 'application/json',
      body: JSON.stringify(formData),
      responseType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    };

    let response = await fetch(
      "http://localhost:8000/schedule_duty",
      requestOptions
    );
    let data = response.body;
    
    const link = document.createElement('a');
    const url = URL.createObjectURL(await response.blob());
    
    link.download = "Duty Calendar";
    link.href = url;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    //setFormData({ video_link: "" });
    
  };

  function appendStaffMember(index, input) {
    staffData[index].name = input;
    setStaffData(staffData);
  }

  function addStaffMember() {
    let data = { name: "", preferences: [""] };
    setStaffData([...staffData, data]);
  }

  function appendDates(index, index2, input) {
    staffData[index].preferences[index2] = input;
    setStaffData(staffData);
  }

  function addDate(index) {
    staffData[index.index].preferences.push(" ");
    setStaffData([...staffData]);
  }

  return (

   <div className ="App-background">
    <Container className="App">
      <Form className="mt-5" onSubmit={(formEvent) => sendFormData(formEvent)}>
        <Form.Label>Duty Scheduling Options</Form.Label>
        <Form.Row>
          <Form.Group>
            <Form.Label>Start Date</Form.Label>
            <Form.Control
              type="date"
              onChange={(inputEvent) =>
                setFormData({ ...formData, startDate: inputEvent.target.value })
              }
            ></Form.Control>
          </Form.Group>

          <Form.Group>
            <Col xs={"auto"}>
              <Form.Label>End Date</Form.Label>
              <Form.Control
                type="date"
                onChange={(inputEvent) =>
                  setFormData({ ...formData, endDate: inputEvent.target.value })
                }
              ></Form.Control>
            </Col>
          </Form.Group>
        </Form.Row>
        <Form.Group className="input-box">
          <Form.Control
            type="text"
            placeholder="Enter Hall Name"
            onChange={(inputEvent) =>
              setFormData({ ...formData, hall: inputEvent.target.value })
            }
          />
        </Form.Group>
        {staffData.map((data, index) => (
          <React.Fragment>
            <Form.Group key={index} className="input-box">
              <Form.Label> Name </Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter staff member name"
                onChange={(inputEvent) =>
                  appendStaffMember(index, inputEvent.target.value)
                }
              />
            </Form.Group>
            <Form.Label>Days Cannot Sit</Form.Label>
            <Form.Row>
              {staffData[index].preferences.map((input, index2) => (
                <React.Fragment>
                  <Col xs="auto">
                    <Form.Group key={index}>
                      <Form.Control
                        type="date"
                        onChange={(inputEvent) =>
                          appendDates(index, index2, inputEvent.target.value)
                        }
                      />
                    </Form.Group>
                  </Col>
                </React.Fragment>
              ))}
              <Col>
                <Button variant="secondary" onClick={() => addDate({ index })}>
                  Add date
                </Button>
              </Col>
            </Form.Row>
          </React.Fragment>
        ))}

        <Button variant="primary" type="submit">
          Submit
        </Button>

        <Button variant="secondary" onClick={addStaffMember}>
          Add staff member
        </Button>
      </Form>
    </Container>
    </div>
    
  );
}

export default App;

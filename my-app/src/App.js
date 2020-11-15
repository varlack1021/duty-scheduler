import React, { Fragment, useState } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
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
      "Content-Type": "application/json",
      body: JSON.stringify(formData),
      responseType:
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    };

    let response = await fetch(
      "http://localhost:8000/schedule_duty",
      requestOptions
    );
    let data = response.body;

    //Download Excel File from website
    const link = document.createElement("a");
    const url = URL.createObjectURL(await response.blob());

    link.download = "Duty Calendar";
    link.href = url;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  //For Some reason I have to use funcs to increase the size of my states
  //If I directly call the functions React crashes with error too many re renders
  function addStaffMember() {
    let data = { name: "", preferences: [""] };
    setStaffData([...staffData, data]);
  }

  function addDate(index) {
    console.log(staffData);
    staffData[index.index].preferences.push("");
    setStaffData([...staffData]);
  }

  function removeStaffMember(index) {
    staffData.splice(index.index, 1);
    setStaffData([...staffData]);
  }
  return (
    <div className="App-background">
      <Container className="App">
        <Form
          className="mt-5"
          onSubmit={(formEvent) => sendFormData(formEvent)}
        >
          <Form.Label>Duty Scheduling Options</Form.Label>
          <Form.Row>
            <Form.Group>
              <Form.Label>Start Date</Form.Label>
              <Form.Control
                type="date"
                required="True"
                onChange={(inputEvent) =>
                  setFormData({
                    ...formData,
                    startDate: inputEvent.target.value,
                  })
                }
              ></Form.Control>
            </Form.Group>

            <Form.Group>
              <Col xs={"auto"}>
                <Form.Label>End Date</Form.Label>
                <Form.Control
                  required="True"
                  type="date"
                  onChange={(inputEvent) =>
                    setFormData({
                      ...formData,
                      endDate: inputEvent.target.value,
                    })
                  }
                ></Form.Control>
              </Col>
            </Form.Group>
          </Form.Row>
          <Form.Row>
            <Form.Group className="input-box">
              <Form.Control
                type="text"
                placeholder="Enter Hall Name"
                onChange={(inputEvent) =>
                  setFormData({ ...formData, hall: inputEvent.target.value })
                }
                value={formData.hall}
              />
            </Form.Group>
          </Form.Row>
          {staffData.map((data, index) => (
            <React.Fragment>
              <Form.Group key={index} className="input-box">
                <Form.Label> Name </Form.Label>

                <Form.Control
                  type="text"
                  required="True"
                  placeholder="Enter staff member name"
                  onChange={(inputEvent) =>
                    setStaffData(
                      staffData.map((item, index2) =>
                        index === index2
                          ? {
                              ...staffData[index],
                              name: inputEvent.target.value,
                            }
                          : item
                      )
                    )
                  }
                  value={staffData[index].name}
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
                            setStaffData(
                              staffData.map((item, index3) =>
                                index === index3
                                  ? {
                                      ...staffData[index],
                                      preferences: item.preferences.map((item2, index4) =>
                                          index2 === index4 ? inputEvent.target.value : item2
                                      )
                                    }
                                  : item
                              )
                            )
                          }
                          value = {staffData[index].preferences[index2]}
                        />
                      </Form.Group>
                    </Col>
                  </React.Fragment>
                ))}
                <Col>
                  <Button
                    variant="secondary"
                    onClick={() => addDate({ index })}
                  >
                    Add date
                  </Button>
                </Col>
              </Form.Row>
              <Form.Row>
                <Col>
                  <Button
                    variant="danger"
                    onClick={() => removeStaffMember({ index })}
                  >
                    Remove Staff Member
                  </Button>
                </Col>
              </Form.Row>
            </React.Fragment>
          ))}

          <Form.Row className="submit-row">
            <Col>
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Col>
            <Col>
              <Button variant="secondary" onClick={addStaffMember}>
                Add staff member
              </Button>
            </Col>
          </Form.Row>
        </Form>
      </Container>
    </div>
  );
}

export default App;

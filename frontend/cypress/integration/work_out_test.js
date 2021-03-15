/// <reference types="cypress" />
let filepath = "PenguinBra.jpg"

context('Actions', () => {
  beforeEach(() => {
    cy.visit('https://tdt4242-axell-vegard-frontend.herokuapp.com/')
    cy.contains("Log in").click()

    cy.get("form").children().first().type("admin")
        .next().type("12345")
        .next().click()
        .next().click()
  })

  /*it('Login', () =>{
    cy.contains("Log in").click()

    cy.get("form").children().first().type("admin")
        .next().type("12345")
        .next().click()
        .next().click()
  })*/

  it('Log new workout', () =>{
    cy.get("#btn-create-workout").click()

    cy.wait(2000)
    cy.get("form").children().first().type("title")
        .next().next().type("2017-06-01T08:30")
        .next().next().next().type("Public")
        .next().type("I did a nice workout without much result")
        .next().next().get('[id="customFile"]')
        .attachFile(filepath)

    cy.get('#btn-ok-workout').click()
  })

  it('Log new workout', () =>{
    cy.get("#btn-create-workout").click()

    cy.wait(2000)
    cy.get("form").children().first().type("dddddddddddddddddddddddddddddddddddddd")
        .next().next().type("2017-06-01T08:30")
        .next().next().next().type("Public")
        .next().type("I did a nice workout without much result")
        .next().next().get('[id="customFile"]')
        .attachFile(filepath)

    cy.get('#btn-ok-workout').click()
  })



  /*it('Login', () => {
    cy.contains('Register').click()

    cy.url().should('include', '/register.html')

    cy.get("form").children().first().type("admin")
        .next().type("admin@gmail.com")
        .next().type("12345")
        .next().type("12345")
        .next().type("12345678")
        .next().type("Norway")
        .next().type("Trondheim")
        .next().type("Astronomveien 1")
        .next().click()
  })*/
})
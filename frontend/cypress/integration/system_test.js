/// <reference types="cypress" />

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

    cy.get("form").children().first().type("admin")
        .next().type("12345")
        .next().click()
        .next().click()
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
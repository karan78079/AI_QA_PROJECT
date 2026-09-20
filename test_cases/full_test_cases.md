# TEST SUITE: Rahul Shetty Academy Client Application

## Application URL
https://rahulshettyacademy.com/client

## Purpose
Use the browser snapshot and these requirements to generate and execute complete pytest Playwright coverage. Execute each scenario as a separate test when possible. Use the supplied credentials only for authentication. Do not hardcode credentials into generated Python source; use `TEST_EMAIL` and `TEST_PASSWORD` environment variables.

## Credentials
- `userEmail`: `rahulshetty@gmail.com`
- `userPassword`: `Iamking@000`

## Test Case 1: Valid Login
**Objective:** Verify that a registered user can successfully log in.

**Steps:**
1. Open the application URL.
2. Verify that the login page is visible.
3. Verify that the email input, password input, and Login button are visible.
4. Enter the valid email from `TEST_EMAIL`.
5. Enter the valid password from `TEST_PASSWORD`.
6. Click the Login button.
7. Wait for the authenticated page to load.
8. Verify that the user is redirected away from the login page.
9. Verify that the product listing page and authenticated navigation are visible.

**Expected Result:** The user is authenticated and redirected to the product listing page.

## Test Case 2: Login Page Validation
**Objective:** Verify that required login fields are validated.

**Steps:**
1. Open the application URL.
2. Leave the email input empty.
3. Leave the password input empty.
4. Click the Login button.
5. Verify that validation feedback is displayed and the user remains on the login page.

**Expected Result:** The application prevents submission when required credentials are empty.

## Test Case 3: Invalid Login
**Objective:** Verify that invalid credentials cannot authenticate a user.

**Test Data:**
- Invalid email: `invalid.user@example.com`
- Invalid password: `InvalidPassword123!`

**Steps:**
1. Open the application URL.
2. Enter the invalid email.
3. Enter the invalid password.
4. Click the Login button.
5. Verify that an authentication error is displayed.
6. Verify that the user remains on the login page.

**Expected Result:** Invalid credentials are rejected and no authenticated page is displayed.

## Test Case 4: Product Listing Page
**Objective:** Verify that products are displayed after login.

**Precondition:** Complete the valid login test successfully.

**Steps:**
1. Log in with `TEST_EMAIL` and `TEST_PASSWORD`.
2. Verify that the product listing page is displayed.
3. Verify that product cards are visible.
4. Verify that each visible product has a product name, price, image, and action button.
5. Verify that the product list is not empty.

**Expected Result:** Authenticated users can view available products and purchase controls.

## Test Case 5: Product Visibility
**Objective:** Verify that a user can identify a product from the product listing.

**Steps:**
1. Log in with `TEST_EMAIL` and `TEST_PASSWORD`.
2. Inspect visible product cards from the browser snapshot.
3. Select one product whose name is present in the current page snapshot.
4. Verify that its product name and price are visible.
5. Verify that its Add To Cart control is visible.

**Expected Result:** A product visible in the live snapshot can be selected. Do not invent product names.

## Test Case 6: Add Product To Cart
**Objective:** Verify that an authenticated user can add a product to the cart.

**Steps:**
1. Log in with `TEST_EMAIL` and `TEST_PASSWORD`.
2. Select a product visible in the listing.
3. Click that product's Add To Cart button.
4. Wait for the cart update or confirmation message.
5. Open the cart.
6. Verify that the selected product appears in the cart.
7. Verify that its name and price match the selected product.
8. Verify that the cart contains one item unless the application reports another quantity.

**Expected Result:** The selected product is added to the cart exactly once.

## Test Case 7: Cart Details
**Objective:** Verify the cart contents and checkout control.

**Precondition:** A product has been added to the cart.

**Steps:**
1. Open the cart page.
2. Verify that the selected product, quantity, price, and total are visible.
3. Verify that the Checkout button is visible and enabled.

**Expected Result:** The cart shows correct information and allows checkout.

## Test Case 8: Checkout Details
**Objective:** Verify that a logged-in user can provide checkout information.

**Precondition:** A product is present in the cart.

**Test Data:** Country: India

**Steps:**
1. Open the cart and click Checkout.
2. Verify that the checkout page and payment/shipping form are visible.
3. Enter valid card details only when fields and approved test data are available.
4. Enter India when a country field is present.
5. Select India from suggestions when autocomplete is used.
6. Verify that the Place Order button is visible.

**Expected Result:** The checkout form accepts valid required information. Do not invent payment data or selectors.

## Test Case 9: Place Order
**Objective:** Verify that a user can place an order for a cart product.

**Precondition:** A product is in the cart and checkout details are complete.

**Steps:**
1. Complete the checkout form with valid available test data.
2. Click Place Order.
3. Wait for confirmation.
4. Verify that confirmation and any order identifier are visible.
5. Verify that no payment or validation error is shown.

**Expected Result:** The order is submitted and confirmation is displayed.

## Test Case 10: Orders Page
**Objective:** Verify that a submitted order is visible in order history.

**Precondition:** The place-order test completed successfully.

**Steps:**
1. Open the Orders page using authenticated navigation.
2. Verify that the Orders page is displayed.
3. Verify that the submitted order or identifier is listed.
4. Open order details when a details control is present.

**Expected Result:** The authenticated user can view order history.

## Test Case 11: Logout
**Objective:** Verify that the user can log out.

**Precondition:** The user is authenticated.

**Steps:**
1. Click the Logout control.
2. Wait for navigation.
3. Verify that the login page is displayed.
4. Verify that authenticated navigation is no longer available.

**Expected Result:** The user is logged out and returned to the login experience.

## Execution Rules
1. Use the live MCP browser snapshot as the source of truth for element names, roles, placeholders, links, buttons, and product names.
2. Do not invent locators, products, order identifiers, payment data, or page text.
3. Use Playwright with pytest.
4. Keep tests independent where possible; log in again for each independent test.
5. Use `TEST_EMAIL` and `TEST_PASSWORD` in generated code.
6. Save generated tests under `generated/tests/`.
7. Validate Python syntax and run pytest collection before execution.
8. Record pass/fail status, stdout, stderr, duration, and traceback.
9. Mark scenarios as blocked when required data is unavailable instead of fabricating data.
10. The final report must identify passed, failed, and blocked scenarios.

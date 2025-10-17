CREATE TABLE EVENT (eventID VARCHAR, eventDescription VARCHAR, eventTimestamp VARCHAR);
INSERT INTO EVENT VALUES ('E1', 'System started', '2025-10-16T09:00:00');
CREATE TABLE INTERACTION (interactionID VARCHAR, interactionDescription VARCHAR, interactionTimestamp VARCHAR, sessionID VARCHAR, deviceID VARCHAR, deviceType VARCHAR, interactionObject VARCHAR);
INSERT INTO INTERACTION VALUES ('I1', 'User clicked button', '2025-10-16T09:05:00', 'S1', 'D1', 'Mobile', 'Button');
CREATE TABLE FULFILLMENT (fulfillmentID VARCHAR, fulfillmentDescription VARCHAR, fulfillmentTimestamp VARCHAR, workflowID VARCHAR, fulfillmentStatus VARCHAR, requestType VARCHAR);
INSERT INTO FULFILLMENT VALUES ('F1', 'Order processed', '2025-10-16T09:10:00', 'W1', 'Completed', 'OrderRequest');

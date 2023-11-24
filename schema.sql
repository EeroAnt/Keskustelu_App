CREATE DATABASE keskustelu_app;
\c keskustelu_app;
CREATE TABLE clearances (id SERIAL PRIMARY KEY, level INTEGER, username TEXT);
CREATE TABLE headers (id SERIAL PRIMARY KEY, header TEXT NOT NULL, topic TEXT NOT NULL, username TEXT NOT NULL);
CREATE TABLE messages (id SERIAL PRIMARY KEY, username TEXT NOT NULL, message TEXT NOT NULL, time TIMESTAMP NOT NULL, header TEXT NOT NULL, topic TEXT NOT NULL);
CREATE TABLE topics (id SERIAL PRIMARY KEY, topic TEXT, secrecy INTEGER);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL, admin BOOLEAN);

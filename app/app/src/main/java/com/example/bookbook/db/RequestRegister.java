package com.example.bookbook.db;

public class RequestRegister {
    private final String email;
    private final String password;
    private final String firstName;
    private final String lastName;

    public RequestRegister(String email, String password, String firstName, String lastName) {
        this.email = email;
        this.password = password;
        this.firstName = firstName;
        this.lastName = lastName;
    }
}

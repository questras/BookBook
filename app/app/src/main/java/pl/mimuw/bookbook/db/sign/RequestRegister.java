package pl.mimuw.bookbook.db.sign;

public class RequestRegister {
    private final String email;
    private final String password;
    private final String first_name;
    private final String last_name;

    public RequestRegister(String email, String password, String firstName, String lastName) {
        this.email = email;
        this.password = password;
        this.first_name = firstName;
        this.last_name = lastName;
    }
}

package pl.mimuw.bookbook.db.main;

public class RequestAddOffer {
    private final String title;
    private final String author;
    private final String description;
    private final String state;
    private final String city;
    private final String lender_phone;

    public RequestAddOffer(String title, String author, String description,
                           String state, String city, String lender_phone) {
        this.title = title;
        this.author = author;
        this.description = description;
        this.state = state;
        this.city = city;
        this.lender_phone = lender_phone;
    }
}

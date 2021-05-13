package pl.mimuw.bookbook.db.main;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import pl.mimuw.bookbook.db.ResponseToken;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.File;
import java.util.ArrayList;

public class MainViewModel extends ViewModel {

    private MutableLiveData<JSONObject> addOfferResp;
    private MutableLiveData<JSONObject> signOutResp;
    private MutableLiveData<ResponseToken> token;
    private MainRepository mainRepository;

    public void init(ResponseToken token) {
        if (mainRepository != null) {
            return;
        }
        mainRepository = MainRepository.getInstance();
        this.token = new MutableLiveData<>(token);
        addOfferResp = new MutableLiveData<>();
        signOutResp = new MutableLiveData<>();
    }

    public LiveData<ResponseToken> getToken() {
        return token;
    }

    public MutableLiveData<JSONObject> getAddOfferResp() {
        return addOfferResp;
    }

    public MutableLiveData<JSONObject> getSignOutResp() {
        return signOutResp;
    }

    public void downloadOffers(MutableLiveData<JSONArray> data) {
        mainRepository.downloadOffers(token.getValue().getToken(), data);
    }

    public void addOffer(String title, String author, String description,
                         String state, String city, String lender_phone) {
        mainRepository.addOffer(title, author, description, state, city,
                lender_phone, token.getValue().getToken(), addOfferResp);
    }

    public void addImage(int id, File imageFile, MutableLiveData<JSONObject> data) {
        mainRepository.addImage(id, imageFile, token.getValue().getToken(), data);
    }


    public void signOut() {
        mainRepository.signOut(token.getValue().getToken(), signOutResp);
    }
}

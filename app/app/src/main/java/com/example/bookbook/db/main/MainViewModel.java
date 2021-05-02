package com.example.bookbook.db.main;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.example.bookbook.db.ResponseToken;

import org.json.JSONObject;

import java.io.File;

public class MainViewModel extends ViewModel {

    private MutableLiveData<JSONObject> addOfferResp;
    private MutableLiveData<ResponseToken> token;
    private MainRepository mainRepository;

    public void init(ResponseToken token) {
        if (mainRepository != null) {
            return;
        }
        mainRepository = MainRepository.getInstance();
        this.token = new MutableLiveData<>(token);
        addOfferResp = new MutableLiveData<>();
    }

    public LiveData<ResponseToken> getToken() {
        return token;
    }

    public MutableLiveData<JSONObject> getAddOfferResp() {
        return addOfferResp;
    }

    public void addOffer(String title, String author, String description,
                         String state, String city, String lender_phone) {
        mainRepository.addOffer(title, author, description, state, city,
                lender_phone, token.getValue().getToken(), addOfferResp);
    }

    public void addImage(int id, File imageFile, MutableLiveData<JSONObject> data) {
        mainRepository.addImage(id, imageFile, token.getValue().getToken(), data);
    }
}

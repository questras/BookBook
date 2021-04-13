package com.example.bookbook.db;

import android.util.Pair;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import org.json.JSONObject;

public class SignViewModel extends ViewModel {

    private MutableLiveData<ResponseToken> token;
    private JSONObject error;
    private SignRepository signRepository;

    public void init() {
        if (signRepository != null) {
            return;
        }
        signRepository = SignRepository.getInstance();
    }

    public LiveData<ResponseToken> getToken() {
        return token;
    }

    public JSONObject getError() {
        return error;
    }

    public void authenticate(String email, String pass) {
        Pair<MutableLiveData<ResponseToken>, JSONObject> response = signRepository.authenticate(email, pass);
        token = response.first;
        error = response.second;
    }

}

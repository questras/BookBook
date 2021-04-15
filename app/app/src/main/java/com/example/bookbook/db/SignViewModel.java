package com.example.bookbook.db;

import android.util.Pair;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import org.json.JSONObject;

public class SignViewModel extends ViewModel {

    private MutableLiveData<Pair<ResponseToken, JSONObject>> token;
    private MutableLiveData<JSONObject> registerResp;
    private SignRepository signRepository;

    public void init() {
        if (signRepository != null) {
            return;
        }
        signRepository = SignRepository.getInstance();
        token = new MutableLiveData<>();
        registerResp = new MutableLiveData<>();
    }

    public LiveData<Pair<ResponseToken, JSONObject>> getToken() {
        return token;
    }

    public void authenticate(String email, String pass) {
        signRepository.authenticate(email, pass, token);
    }

    public MutableLiveData<JSONObject> getRegisterResp() {
        return registerResp;
    }

    public void register(String email, String pass, String firstName, String lastName) {
        signRepository.register(email, pass, firstName, lastName, registerResp);
    }
}

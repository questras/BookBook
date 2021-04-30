package com.example.bookbook;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.google.android.material.button.MaterialButton;

public class NewOffer extends Fragment {
    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_new_offer, container, false);
        MaterialButton addOfferButton = view.findViewById(R.id.add_offer_button);

        addOfferButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ((MainActivity) requireActivity()).navigateTo(R.id.add_successful);
            }
        });

        return view;
    }
}

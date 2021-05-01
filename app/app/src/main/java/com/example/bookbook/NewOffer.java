package com.example.bookbook;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.example.bookbook.db.main.MainViewModel;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Arrays;

public class NewOffer extends Fragment {
    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_new_offer, container, false);
        MaterialButton addOfferButton = view.findViewById(R.id.add_offer_button);
        MainViewModel model = new ViewModelProvider(requireActivity()).get(MainViewModel.class);
        model.getAddOfferResp().observe(requireActivity(), new ResponesObserver(view));

        addOfferButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                model.addOffer(((TextInputEditText) view.findViewById(R.id.book_title_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.book_author_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.state_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.city_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.description_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.phone_edit_text)).getText().toString());
            }
        });

        return view;
    }

    static class ResponesObserver implements Observer<JSONObject> {
        private final ArrayList<TextInputLayout> textFields;
        private final ArrayList<String> fieldNames = new ArrayList<String>(
                Arrays.asList("title", "author", "description", "state", "city", "lender_phone"));

        public ResponesObserver(View view) {
            textFields = new ArrayList<>();
            textFields.add(view.findViewById(R.id.book_title_text_input));
            textFields.add(view.findViewById(R.id.book_author_text_input));
            textFields.add(view.findViewById(R.id.state_text_input));
            textFields.add(view.findViewById(R.id.city_text_input));
            textFields.add(view.findViewById(R.id.description_text_input));
            textFields.add(view.findViewById(R.id.phone_text_input));
        }

        @Override
        public void onChanged(JSONObject response) {
            if (response != null) {
                for (int i = 0; i < fieldNames.size(); i++) {
                    if (response.has(fieldNames.get(i)))
                        textFields.get(i).setError(response.optJSONArray(fieldNames.get(i)).optString(0));
                    else
                        textFields.get(i).setError(null);
                }
            }
        }

    }
}

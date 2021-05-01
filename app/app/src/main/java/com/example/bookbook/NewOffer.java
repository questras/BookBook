package com.example.bookbook;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.example.bookbook.db.main.MainViewModel;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.sql.Struct;
import java.util.ArrayList;
import java.util.Arrays;

public class NewOffer extends Fragment {

    public static final int REQUEST_IMAGE_CAPTURE = 1;
    private Bitmap offerImageToDisplay;
    private String offerImageToSend;
    private ImageButton addPhotoButton;

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_new_offer, container, false);
        offerImageToSend = null;
        MaterialButton addOfferButton = view.findViewById(R.id.add_offer_button);
        addPhotoButton = view.findViewById(R.id.add_photo_button);
        MainViewModel model = new ViewModelProvider(requireActivity()).get(MainViewModel.class);
        model.getAddOfferResp().observe(requireActivity(), new AddOfferResponseObserver(view, offerImageToSend));

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

        addPhotoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                if (takePictureIntent.resolveActivity(requireActivity().getPackageManager()) != null) {
                    startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
                }
            }
        });

        return view;
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == -1) {
            Bundle extras = data.getExtras();
            offerImageToDisplay = (Bitmap) extras.get("data");
            addPhotoButton.setImageBitmap(Bitmap.createScaledBitmap(offerImageToDisplay, 500, 500, true));
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            offerImageToDisplay.compress(Bitmap.CompressFormat.PNG, 90, stream); //compress to which format you want.
            byte[] byteArr = stream.toByteArray();
            offerImageToSend = Base64.encodeToString(byteArr, Base64.DEFAULT);
        }
    }

    static class AddImageResponseObserver implements Observer<JSONObject> {
        @Override
        public void onChanged(JSONObject response) {
            if (!response.has("id")) {
                Log.d("Image", "Couldn't send image to db");
            }
        }
    }

    class AddOfferResponseObserver implements Observer<JSONObject> {
        private final ArrayList<TextInputLayout> textFields;
        private final ArrayList<String> fieldNames = new ArrayList<String>(
                Arrays.asList("title", "author", "description", "state", "city", "lender_phone"));
        private final String offerImageToSend;

        public AddOfferResponseObserver(View view, String offerImageToSend) {
            textFields = new ArrayList<>();
            textFields.add(view.findViewById(R.id.book_title_text_input));
            textFields.add(view.findViewById(R.id.book_author_text_input));
            textFields.add(view.findViewById(R.id.state_text_input));
            textFields.add(view.findViewById(R.id.city_text_input));
            textFields.add(view.findViewById(R.id.description_text_input));
            textFields.add(view.findViewById(R.id.phone_text_input));
            this.offerImageToSend = offerImageToSend;
        }

        @Override
        public void onChanged(JSONObject response) {
            if (response != null && !response.has("id")) {
                for (int i = 0; i < fieldNames.size(); i++) {
                    if (response.has(fieldNames.get(i))) {
                        textFields.get(i).setError(response.optJSONArray(fieldNames.get(i)).optString(0));
                    } else
                        textFields.get(i).setError(null);
                }
            }

            if (response != null && response.has("id") && offerImageToSend != null) {
                new ViewModelProvider(requireActivity()).get(MainViewModel.class).addImage(
                        response.optInt("id"), offerImageToSend, new MutableLiveData<>());
            }
        }
    }

}

package pl.mimuw.bookbook.ui;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import pl.mimuw.bookbook.R;
import pl.mimuw.bookbook.db.main.MainViewModel;
import pl.mimuw.bookbook.db.main.Offer;

public class SearchEngine extends Fragment {

    private MainViewModel model;

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_search_engine, container, false);
        MutableLiveData<JSONArray> offersRaw = new MutableLiveData<>();
        model = new ViewModelProvider(requireActivity()).get(MainViewModel.class);
        offersRaw.observe(requireActivity(), this::handleNewOffers);
        model.downloadOffers(offersRaw);

        return view;
    }

    private void handleNewOffers(JSONArray data) {
        if (data == null) {
            return;
        }

        ArrayList<Offer> offers = new ArrayList<>();
        for (int i = 0; i < data.length(); i++) {
            try {
                JSONObject offerJson = data.getJSONObject(i);
                if (!offerJson.getString("status").equals(Offer.activeStatus))
                    continue;
                JSONObject lenderJson = offerJson.getJSONObject("lender");
                String imageUrl;
                if (offerJson.getJSONArray("images").length() > 0) {
                    imageUrl = offerJson.getJSONArray("images").
                            getJSONObject(0).getString("image");
                } else {
                    imageUrl = "";
                }
                offers.add(new Offer(offerJson.getInt("id"), imageUrl,
                        offerJson.getString("title"), offerJson.getString("author"),
                        offerJson.getString("description"), offerJson.getString("state"),
                        offerJson.getString("city"), lenderJson.getString("email"),
                        lenderJson.getString("first_name"), lenderJson.getString("last_name"),
                        offerJson.getString("lender_phone")));
            } catch (JSONException e) {
                Log.d("JSON", "Error during data conversion");
            }
        }
        model.setOffers(offers);
        model.clearOffersImages();

        RecyclerView offerRv = requireActivity().findViewById(R.id.offerRv);
        offerRv.setNestedScrollingEnabled(false);
        offerRv.setLayoutManager(new LinearLayoutManager(requireActivity()));
        offerRv.setAdapter(new BrowseAdapter(requireActivity(), offers));
    }
}

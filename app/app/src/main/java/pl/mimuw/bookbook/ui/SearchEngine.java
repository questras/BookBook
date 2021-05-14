package pl.mimuw.bookbook.ui;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.core.widget.NestedScrollView;
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
    private BrowseAdapter adapter;
    private RecyclerView offerRv;
    private NestedScrollView outerScroll;

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_search_engine, container, false);
        outerScroll = view.findViewById(R.id.outer_scroll);
        initScrollListener();
        offerRv = view.findViewById(R.id.offerRv);
        offerRv.setNestedScrollingEnabled(false);
        offerRv.setLayoutManager(new LinearLayoutManager(requireActivity()));
        adapter = new BrowseAdapter(requireActivity());
        offerRv.setAdapter(adapter);

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
        ArrayList<Offer> offers = parseOffersJson(data);

//        First data set up
        for (int i = 0; i < Math.min(10, offers.size() - adapter.offers.size()); i++) {
            adapter.offers.add(offers.get(adapter.offers.size()));
        }
        adapter.notifyDataSetChanged();

        model.setOffers(offers);
        model.clearOffersImages();
    }

    private ArrayList<Offer> parseOffersJson(JSONArray data) {
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
        return offers;
    }

    private void initScrollListener() {
        outerScroll.setOnScrollChangeListener(new NestedScrollView.OnScrollChangeListener() {
            @Override
            public void onScrollChange(NestedScrollView v, int scrollX, int scrollY, int oldScrollX, int oldScrollY) {
                int diff = v.getChildAt(0).getMeasuredHeight() - v.getMeasuredHeight();
                if (scrollY == diff) {
                    int toAdd = Math.min(10, model.getOffers().size() - adapter.offers.size());
                    for (int i = 0; i < toAdd; i++) {
                        adapter.offers.add(model.getOffers().get(adapter.offers.size()));
                    }
                    if (toAdd > 0) {
                        adapter.notifyDataSetChanged();
                    } else {
                        Toast.makeText(requireActivity(), "No more offers!", Toast.LENGTH_LONG).show();
                    }
                }
            }
        });
    }
}

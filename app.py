import streamlit as st
from policyengine_us import Simulation
import pandas as pd
import plotly.express as px


@st.cache_data
def calculate_net_incomes():
    def calculate_net_income(state):
        situation = {
            "people": {
                "you": {
                    "age": {"2024": 40},
                    "employment_income": {"2024": 25000},
                    "pre_subsidy_rent": {"2024": 24000},
                },
                "your partner": {
                    "age": {"2024": 40},
                    "employment_income": {"2024": 25000},
                },
                "your first dependent": {"age": {"2024": 2}},
                "your second dependent": {"age": {"2024": 4}},
            },
            "families": {
                "your family": {
                    "members": [
                        "you",
                        "your partner",
                        "your first dependent",
                        "your second dependent",
                    ]
                }
            },
            "marital_units": {
                "your marital unit": {"members": ["you", "your partner"]},
                "your first dependent's marital unit": {
                    "members": ["your first dependent"],
                    "marital_unit_id": {"2024": 1},
                },
                "your second dependent's marital unit": {
                    "members": ["your second dependent"],
                    "marital_unit_id": {"2024": 2},
                },
            },
            "tax_units": {
                "your tax unit": {
                    "members": [
                        "you",
                        "your partner",
                        "your first dependent",
                        "your second dependent",
                    ]
                }
            },
            "spm_units": {
                "your household": {
                    "members": [
                        "you",
                        "your partner",
                        "your first dependent",
                        "your second dependent",
                    ],
                    "spm_unit_capped_work_childcare_expenses": {"2024": 6000},
                }
            },
            "households": {
                "your household": {
                    "members": [
                        "you",
                        "your partner",
                        "your first dependent",
                        "your second dependent",
                    ],
                    "state_name": {"2024": state},
                }
            },
        }

        simulation = Simulation(situation=situation)
        output = simulation.calculate("household_net_income", 2024)
        return float(output)

    states = [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    ]

    net_incomes = {}
    for state in states:
        net_incomes[state] = calculate_net_income(state)

    return net_incomes


st.title("Household Net Income by State")

st.markdown(
    """
The household consists of:
- Two married adults, both age 40 with \$25,000 in wages
- Two children, age 2 and 4
- Monthly expenses of \$2,000 for rent and \$500 for childcare
"""
)

net_incomes = calculate_net_incomes()

states = list(net_incomes.keys())
selected_state = st.selectbox("Select a state for comparison:", states)

df = pd.DataFrame(list(net_incomes.items()), columns=["State", "Net Income"])

reference_income = net_incomes[selected_state]
df["Difference"] = df["Net Income"] - reference_income

fig = px.choropleth(
    df,
    locations="State",
    locationmode="USA-states",
    color="Difference",
    scope="usa",
    color_continuous_scale=px.colors.diverging.RdBu,
    color_continuous_midpoint=0,
    labels={"Difference": "Difference ($)", "Net Income": "Net Income ($)"},
    title=f"Household Net Income Difference Compared to {selected_state}",
    hover_data={"State": True, "Difference": ":.2f", "Net Income": ":.2f"},
)

st.plotly_chart(fig)

st.markdown(
    """
Data and calculations provided by [PolicyEngine](https://policyengine.org/).
"""
)

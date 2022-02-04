#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


#MISSING PROGRAM WEBSITES: NMCP - Otolaryngology, Urology; Travis AFB - Orthopaedic Surgery

import folium
from folium import Circle, Marker
import pandas
import branca
import ipywidgets as widgets
from IPython.display import display, clear_output
import voila

search_specialty = ""
usu_aoa = "Click " + "<a href=http://www.usuaoa.org/program-previews>here</a>" + " to access the USU AOA Program Preview Catalog for military residencies!"


specialty_list = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(specialties).csv")
specialty = widgets.Dropdown(options=specialty_list['Specialty'].tolist(),description='Specialty:')
map_All = widgets.Button(description='All Programs')
branch_Army = widgets.Button(description='Army')
branch_AirForce = widgets.Button(description='Air Force')
branch_Navy = widgets.Button(description='Navy')
out = widgets.Output()
def All_clicked(_):
    with out:
        clear_output()
        df = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(all%20programs).csv")
        m_2 = folium.Map(location=[37, -119], zoom_start=3, min_zoom=3)
        folium.Marker(location=[55, -150], popup=usu_aoa, color="red").add_to(m_2)
        for lat, lon, color, popup in zip(df['Longitude'],df['Latitude'],df['Color'],df['Popup']):
            popup_html = popup
            iframe = branca.element.IFrame(html=popup_html, width=350, height=200)
            pop_up = folium.Popup(iframe)
            folium.CircleMarker(location=[lat,lon], radius=5, popup=pop_up, color=color, fill=True, fill_opacity=1).add_to(m_2)
        display(m_2)
def specialty_clicked(_):
    with out:
        clear_output()
        search_specialty = specialty.value
        m_2 = folium.Map(location=[37, -119], zoom_start=3, min_zoom=3)
        folium.Marker(location=[55, -150], popup=usu_aoa, color="red").add_to(m_2)
        df = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(by%20specialty).csv")
        df = df[df['Specialty'].str.contains(search_specialty)]
        for lat, lon, color, website, name, joint_Army, joint_AirForce, joint_Navy, AirForce_spots, Navy_spots in zip(df['Longitude'],df['Latitude'],df['Color'],df['Website'],df["Specialty"],df["Army"],df["Air Force"],df["Navy"], df["Air Force spots available (2022)"], df["Navy spots available (2022)"]):
            popup_html = "<a href=" + str(website) + ">" + name + "</a>"
            if color == "green" and joint_AirForce > 0 and joint_Navy < 1:
                popup_html = "<a href=" + str(website) + ">" + name + "</a><br>(joint Air Force)"
                if str(AirForce_spots) != "NaN":
                    popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots)
            if color == "green" and joint_AirForce > 0 and joint_Navy > 0:
                popup_html = "<a href=" + str(website) + ">" + name + "</a><br>(joint Air Force and Navy)"
                if str(AirForce_spots) != "NaN" and str(Navy_spots) != "NaN":
                    popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots) + "<br><br>Navy spots available (2022): " + str(Navy_spots)
            if color == "green" and joint_AirForce < 1 and joint_Navy > 0:
                popup_html = "<a href=" + str(website) + ">" + name + "</a><br>(joint Navy)"
                if str(Navy_spots) != "NaN":
                    popup_html = popup_html + "<br><br>Navy spots available (2022):" + str(Navy_spots)
            if color == "blue":
                if str(AirForce_spots) != "NaN":
                    popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots)
            if color == "yellow" and joint_AirForce > 0:
                popup_html = "<a href=" + str(website) + ">" + name + "</a><br>(joint Air Force)"
                if str(AirForce_spots) != "NaN" and str(Navy_spots) != "NaN":
                    popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots) + "<br><br>Navy spots available (2022): " + str(Navy_spots)
            if color == "yellow" and joint_AirForce < 1:
                popup_html = "<a href=" + str(website) + ">" + name + "</a><br><br>Navy spots available (2022): " + str(Navy_spots)
            iframe = branca.element.IFrame(html=popup_html, width=300, height=150)
            pop_up = folium.Popup(iframe)
            folium.CircleMarker(location=[lat,lon], radius=5, popup=pop_up, color=color, fill=True, fill_opacity=1).add_to(m_2)
            df_boards = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Army%20GME%20Data%20-%20Boards.csv")
            df_match = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Army%20GME%20Data%20-%20Match%20Results.csv")
            title = "Army " + search_specialty
            def full_popup_html(boards, match):
                step=df_boards['2021 USMLE Step 2 - Mean (Range)'].iloc[boards] 
                comlex=df_boards['2021 COMLEX Level 2 - Mean (Range)'].iloc[boards]
                positions = df_match['Positions Offered (2021)'].iloc[match] 
                ratio_2015=df_match['2015'].iloc[match] 
                ratio_2016=df_match['2016'].iloc[match] 
                ratio_2017=df_match['2017'].iloc[match] 
                ratio_2018=df_match['2018'].iloc[match] 
                ratio_2019=df_match['2019'].iloc[match] 
                ratio_2020=df_match['2020'].iloc[match] 
                ratio_2021=df_match['2021'].iloc[match] 

                left_col_color = "#19a7bd"
                right_col_color = "#f2f0d3"

                html = """<!DOCTYPE html>
            <html>

            <head>
            <h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(title) + """

            </head>
                <table style="height: 126px; width: 350px;">
            <tbody>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2021 USMLE Step 2 - Mean (Range)</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(step) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2021 COMLEX Level 2 - Mean (Range)</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(comlex) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Positions Offered (2021)</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(positions) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2015 - Applicants/Positions</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2015) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2016 - Applicants/Positions</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2016) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2017 - Applicants/Positions</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2017) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2018 - Applicants/Positions</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2018) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2019 - Applicants/Positions</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2019) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2020 - Applicants/Positions</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2020) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2021 - Applicants/Positions</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2021) + """
            </tr>
            </tbody>
            </table>
            </html>
            """
                return html
            if search_specialty in df_boards.values:
                table_html = full_popup_html(df_boards[df_boards['Specialty'] == search_specialty].index[0], df_match[df_match['Specialty'] == search_specialty].index[0])
                table_iframe = branca.element.IFrame(html=table_html, width=375, height=375)
                table_pop_up = folium.Popup(table_iframe)
                folium.Marker(location=[50, -150], popup=table_pop_up).add_to(m_2)
        display(m_2)
def Army_clicked(_):
    with out:
        clear_output()
        search_specialty = specialty.value
        m_2 = folium.Map(location=[37, -119], zoom_start=3, min_zoom=3)
        folium.Marker(location=[55, -150], popup=usu_aoa, color="red").add_to(m_2)
        if search_specialty == "All":
            df = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(all%20programs).csv")
            df = df[df['Color'].str.contains("green")]
            for lat, lon, color, popup in zip(df['Longitude'],df['Latitude'],df['Color'],df['Popup']):
                popup_html = popup
                iframe = branca.element.IFrame(html=popup_html, width=350, height=200)
                pop_up = folium.Popup(iframe)
                folium.CircleMarker(location=[lat,lon], radius=5, popup=pop_up, color=color, fill=True, fill_opacity=1).add_to(m_2)
            display(m_2)
        else:
            df = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(by%20specialty).csv")
            df = df[df['Army'].astype(int) > 0]
            df = df[df['Specialty'].str.contains(search_specialty)]
            for lat, lon, color, website, name, joint_Army, joint_AirForce, joint_Navy, AirForce_spots, Navy_spots in zip(df['Longitude'],df['Latitude'],df['Color'],df['Website'],df["Specialty"],df["Army"],df["Air Force"],df["Navy"], df["Air Force spots available (2022)"], df["Navy spots available (2022)"]):
                popup_html = "<a href=" + str(website) + ">" + name + "</a>"
                if color == "green" and joint_AirForce > 0 and joint_Navy < 1:
                    popup_html = "<a href=" + str(website) + ">" + name + "</a><br>(joint Air Force)"
                    if str(AirForce_spots) != "NaN":
                        popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots)
                if color == "green" and joint_AirForce > 0 and joint_Navy > 0:
                    popup_html = "<a href=" + str(website) + ">" + name + "</a><br>(joint Air Force and Navy)"
                    if str(AirForce_spots) != "NaN" and str(Navy_spots) != "NaN":
                        popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots) + "<br><br>Navy spots available (2022): " + str(Navy_spots)
                if color == "green" and joint_AirForce < 1 and joint_Navy > 0:
                    popup_html = "<a href=" + str(website) + ">" + name + "</a><br>(joint Navy)"
                    if str(Navy_spots) != "NaN":
                        popup_html = popup_html + "<br><br>Navy spots available (2022):" + str(Navy_spots)
                if color == "blue":
                    if str(AirForce_spots) != "NaN":
                        popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots)
                if color == "yellow" and joint_AirForce > 0:
                    popup_html = "<a href=" + str(website) + ">" + name + "</a><br>(joint Air Force)"
                    if str(AirForce_spots) != "NaN" and str(Navy_spots) != "NaN":
                        popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots) + "<br><br>Navy spots available (2022): " + str(Navy_spots)
                if color == "yellow" and joint_AirForce < 1:
                    popup_html = "<a href=" + str(website) + ">" + name + "</a><br><br>Navy spots available (2022): " + str(Navy_spots)
                iframe = branca.element.IFrame(html=popup_html, width=300, height=150)
                pop_up = folium.Popup(iframe)
                folium.CircleMarker(location=[lat,lon], radius=5, popup=pop_up, color=color, fill=True, fill_opacity=1).add_to(m_2)
                df_boards = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Army%20GME%20Data%20-%20Boards.csv")
                df_match = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Army%20GME%20Data%20-%20Match%20Results.csv")
                title = "Army " + search_specialty
                def full_popup_html(boards, match):
                    step=df_boards['2021 USMLE Step 2 - Mean (Range)'].iloc[boards] 
                    comlex=df_boards['2021 COMLEX Level 2 - Mean (Range)'].iloc[boards]
                    positions = df_match['Positions Offered (2021)'].iloc[match] 
                    ratio_2015=df_match['2015'].iloc[match] 
                    ratio_2016=df_match['2016'].iloc[match] 
                    ratio_2017=df_match['2017'].iloc[match] 
                    ratio_2018=df_match['2018'].iloc[match] 
                    ratio_2019=df_match['2019'].iloc[match] 
                    ratio_2020=df_match['2020'].iloc[match] 
                    ratio_2021=df_match['2021'].iloc[match] 

                    left_col_color = "#19a7bd"
                    right_col_color = "#f2f0d3"

                    html = """<!DOCTYPE html>
                <html>

                <head>
                <h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(title) + """

                </head>
                    <table style="height: 126px; width: 350px;">
                <tbody>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2021 USMLE Step 2 - Mean (Range)</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(step) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2021 COMLEX Level 2 - Mean (Range)</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(comlex) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Positions Offered (2021)</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(positions) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2015 - Applicants/Positions</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2015) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2016 - Applicants/Positions</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2016) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2017 - Applicants/Positions</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2017) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2018 - Applicants/Positions</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2018) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2019 - Applicants/Positions</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2019) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2020 - Applicants/Positions</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2020) + """
                </tr>
                <tr>
                <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">2021 - Applicants/Positions</span></td>
                <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(ratio_2021) + """
                </tr>
                </tbody>
                </table>
                </html>
                """
                    return html
                if search_specialty in df_boards.values:
                    table_html = full_popup_html(df_boards[df_boards['Specialty'] == search_specialty].index[0], df_match[df_match['Specialty'] == search_specialty].index[0])
                    table_iframe = branca.element.IFrame(html=table_html, width=375, height=375)
                    table_pop_up = folium.Popup(table_iframe)
                    folium.Marker(location=[50, -150], popup=table_pop_up).add_to(m_2)
            display(m_2)
def AirForce_clicked(_):
    with out:
        clear_output()
        search_specialty = specialty.value
        m_2 = folium.Map(location=[37, -119], zoom_start=3, min_zoom=3)
        folium.Marker(location=[55, -150], popup=usu_aoa, color="red").add_to(m_2)
        if search_specialty == "All":
            df = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(all%20programs).csv")
            df = df[df['Color'].str.contains("blue")]
            for lat, lon, color, popup in zip(df['Longitude'],df['Latitude'],df['Color'],df['Popup']):
                popup_html = popup
                iframe = branca.element.IFrame(html=popup_html, width=350, height=200)
                pop_up = folium.Popup(iframe)
                folium.CircleMarker(location=[lat,lon], radius=5, popup=pop_up, color=color, fill=True, fill_opacity=1).add_to(m_2)
            display(m_2)
        else:
            df = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(by%20specialty).csv")
            df = df[df['Air Force'].astype(int) > 0]
            df = df[df['Specialty'].str.contains(search_specialty)]
            for lat, lon, color, website, name, joint_Army, joint_AirForce, joint_Navy, AirForce_spots, Navy_spots in zip(df['Longitude'],df['Latitude'],df['Color'],df['Website'],df["Specialty"],df["Army"],df["Air Force"],df["Navy"], df["Air Force spots available (2022)"], df["Navy spots available (2022)"]):
                popup_html = "<a href=" + str(website) + ">" + name + "</a>"
                if joint_Army > 0 and joint_Navy < 1:
                    popup_html = popup_html + "<br>(joint Air Force)<br><br>Air Force spots available (2022): " + str(AirForce_spots)
                if joint_Army > 0 and joint_Navy > 0:
                    popup_html = popup_html + "<br>(joint Air Force and Navy)<br><br>Air Force spots available (2022): " + str(AirForce_spots)
                if joint_Army < 1 and joint_Navy > 0:
                    popup_html = popup_html + "<br>(joint Navy)<br><br>Air Force spots available (2022): " + str(AirForce_spots)
                if joint_Army < 1 and joint_Navy < 1:
                    popup_html = popup_html + "<br><br>Air Force spots available (2022): " + str(AirForce_spots)
                iframe = branca.element.IFrame(html=popup_html, width=200, height=150)
                pop_up = folium.Popup(iframe, max_width=200)
                folium.CircleMarker(location=[lat,lon], radius=5, popup=pop_up, color=color, fill=True, fill_opacity=1).add_to(m_2)
            display(m_2)
def Navy_clicked(_):
    with out:
        clear_output()
        search_specialty = specialty.value
        m_2 = folium.Map(location=[37, -119], zoom_start=3, min_zoom=3)
        folium.Marker(location=[55, -150], popup=usu_aoa, color="red").add_to(m_2)
        if search_specialty == "All":
            df = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(all%20programs).csv")            
            df = df[df['Color'].str.contains("yellow")]
            for lat, lon, color, popup in zip(df['Longitude'],df['Latitude'],df['Color'],df['Popup']):
                popup_html = popup
                iframe = branca.element.IFrame(html=popup_html, width=350, height=200)
                pop_up = folium.Popup(iframe)
                folium.CircleMarker(location=[lat,lon], radius=5, popup=pop_up, color=color, fill=True, fill_opacity=1).add_to(m_2)
            display(m_2)
        else:
            df = pandas.read_csv("https://raw.githubusercontent.com/pc3541/Military-Residencies-Map/main/Military%20Residencies%20-%20Map%20(by%20specialty).csv")
            df = df[df['Navy'].astype(int) > 0]
            df = df[df['Specialty'].str.contains(search_specialty)]
            for lat, lon, color, website, name, joint_Army, joint_AirForce, joint_Navy, AirForce_spots, Navy_spots in zip(df['Longitude'],df['Latitude'],df['Color'],df['Website'],df["Specialty"],df["Army"],df["Air Force"],df["Navy"], df["Air Force spots available (2022)"], df["Navy spots available (2022)"]):
                popup_html = "<a href=" + str(website) + ">" + name + "</a>"
                if joint_Army > 0 and joint_AirForce < 1:
                    popup_html = popup_html + "<br>(joint Navy)<br><br>Navy spots available (2022):" + str(Navy_spots)
                if joint_Army > 0 and joint_AirForce > 0:
                    popup_html = popup_html + "<br>(joint Air Force and Navy)<br><br>Navy spots available (2022):" + str(Navy_spots)
                if joint_Army < 1 and joint_AirForce > 0:
                    popup_html = popup_html + "<br>(joint Air Force)<br><br>Navy spots available (2022):" + str(Navy_spots)
                if joint_Army < 1 and joint_AirForce < 1:
                    popup_html = popup_html + "<br><br>Navy spots available (2022): " + str(Navy_spots)
                iframe = branca.element.IFrame(html=popup_html, width=200, height=150)
                pop_up = folium.Popup(iframe, max_width=200)
                folium.CircleMarker(location=[lat,lon], radius=5, popup=pop_up, color=color, fill=True, fill_opacity=1).add_to(m_2)
            display(m_2)
specialty.on_trait_change(specialty_clicked, name="value")
map_All.on_click(All_clicked)
branch_Army.on_click(Army_clicked)
branch_AirForce.on_click(AirForce_clicked)
branch_Navy.on_click(Navy_clicked)
display(widgets.VBox([map_All, specialty, branch_Army, branch_AirForce, branch_Navy, out]))


# In[ ]:





# In[ ]:





# In[ ]:





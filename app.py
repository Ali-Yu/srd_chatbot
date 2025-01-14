import streamlit as st
import os
import importlib.util
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 动态加载模块函数
def load_module(module_name, module_path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 加载模块
replace_module = load_module("replace_module", "./#4_replacement.py")
nature_to_cypher_module = load_module("nature_to_cypher_module", "./#5_nature_to_cypher.py")
query_execution_module = load_module("query_execution_module", "./#6_query_execution.py")
restructure_module = load_module("restructure_module", "./#7_restructure.py")

# Streamlit App
st.title("心理健康相关工作流")

# 用户输入
user_input = st.text_area("请输入文本进行主题判定：")

if user_input:
    # 动态加载其他模块
    topic_module = load_module("topic_module", "./#0_topic.py")
    translate_module = load_module("translate_module", "./#1_translate.py")
    classify_module = load_module("classify_module", "./#2_classify.py")

    # 主题判定
    if topic_module.is_mental_health_related(user_input):
        st.success("主题判定结果：与心理健康相关。")

        # 翻译模块
        translated_text = translate_module.translate_input(user_input)
        st.write(f"翻译结果：{translated_text}")

        # 分类模块
        classification_result = classify_module.classify_input(translated_text)
        st.write(f"分类结果：{classification_result}")

        # 映射模块选择与结果
        mapped_terms = []
        if "Disorder" in classification_result:
            disorder_module = load_module("disorder_module", "./#3_1_mapping_disorder.py")
            disorder_result = disorder_module.map_disorder_terms(translated_text)
            st.write(f"Disorder mapping结果：{disorder_result}")
            mapped_terms.append(disorder_result)

        if "Treatment" in classification_result:
                treatment_module = load_module("treatment_module", "./#3_6_mapping_treat.py")
                treatment_result = treatment_module.map_treatment_terms(translated_text)
                print(f"Treatment mapping结果：{treatment_result}")
                mapped_terms.append(treatment_result)

        if "Biomarker" in classification_result:
            biomarker_module = load_module("biomarker_module", "./#3_2_mapping_biomarker.py")
            biomarker_result = biomarker_module.map_biomarker_terms(translated_text)
            print(f"Biomarker mapping结果：{biomarker_result}")
            mapped_terms.append(biomarker_result)

        if "Measurement" in classification_result:
            measurement_module = load_module("measurement_module", "./#3_3_mapping_measure.py")
            measurement_result = measurement_module.map_measure_terms(translated_text)
            print(f"Measurement mapping结果：{measurement_result}")
            mapped_terms.append(measurement_result)

        if "RiskFactor" in classification_result:
            risk_module = load_module("risk_module", "./#3_4_mapping_risk.py")
            risk_result = risk_module.map_riskfactor_terms(translated_text)
            print(f"RiskFactor mapping结果：{risk_result}")
            mapped_terms.append(risk_result)

        if "Symptom" in classification_result:
            symptom_module = load_module("symptom_module", "./#3_5_mapping_symptom.py")
            symptom_result = symptom_module.map_symptom_terms(translated_text)
            print(f"Symptom mapping结果：{symptom_result}")
            mapped_terms.append(symptom_result)

        # 合并所有映射结果
        all_mapped_terms = "\n".join(mapped_terms)

        # 替换模块
        replaced_text = replace_module.replace_with_mapped_terms(translated_text, all_mapped_terms)
        st.write(f"替换后的文本：{replaced_text}")

        # 转换为 Cypher 查询
        cypher_query = nature_to_cypher_module.natural_language_to_cypher(replaced_text)
        st.write(f"生成的 Cypher 查询：{cypher_query}")

        # 执行查询
        query_results = query_execution_module.execute_query(cypher_query)
        st.write("查询结果：", query_results)

        # 构建 Enhanced Prompt
        enhanced_prompt = restructure_module.build_enhanced_prompt(user_input, query_results)
        st.write(f"构建的 Enhanced Prompt：\n{enhanced_prompt}")

        # 调用 LLM 并获取响应
        llm_response = restructure_module.invoke_llm(enhanced_prompt)
        st.write(f"LLM 输出结果：\n{llm_response}")

    else:
        st.warning("主题判定结果：与心理健康无关，请重新输入。")

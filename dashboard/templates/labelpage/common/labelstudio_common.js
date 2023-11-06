function getLabelstudioConfig(question, answer, risk_level) {
    const single_dialogs =
        `<div style=\"max-width: 100%\">
            <div style=\"clear: both\">
                <div style=\"display: inline-block; background-color: #fff; border-radius: 12px 12px 12px 0; padding: 12px 18px; margin: 10px 0; max-width: 80%; color: rgba(18, 19, 22, 0.50)\">
                    <p>
                        ${question}
                    </p>
                </div>
            </div>
            <div style=\"clear: both\">
                <div style=\"float: right; display: inline-block; background-color: #fff; border-radius: 12px 12px 0 12px; padding: 12px 18px; margin: 10px 0; max-width: 80%; color: rgba(18, 19, 22, 0.50)\">
                    <p>
                        ${answer}
                    </p>
                </div>
            </div>
        </div>`;
            // rank标注
    const plural_dialogs =
        `<div style=\"max-width: 100%\">
            <div style=\"clear: both\">
                <div style=\"display: inline-block; background-color: #fff; border-radius: 12px 12px 12px 0; padding: 12px 18px; margin: 10px 0; max-width: 80%; color: rgba(18, 19, 22, 0.50)\">
                    <p>
                        ${question}
                    </p>
                </div>
            </div>
            <div style=\"float: right; width: 80%;\">
                <div>回答1</div>
                <div style=\"clear: both\">
                    <div style=\"float: right; background-color: #fff; border-radius: 12px 12px 0 12px; padding: 12px 18px; margin: 10px 0; color: rgba(18, 19, 22, 0.50); width: calc(100% - 36px)\">
                        <p>
                            ${answer}
                        </p>
                    </div>
                </div>
            </div>
        </div>`;

    // safe标注
    const safe_dialog =
        `<div style=\"max-width: 100%\">
            <div style=\"clear: both\">
                <div style=\"display: inline-block; background-color: #fff; border-radius: 12px 12px 12px 0; padding: 12px 18px; margin: 10px 0; max-width: 80%; color: rgba(18, 19, 22, 0.50)\">
                    <p>
                        ${question}
                    </p>
                </div>
            </div>
            <div style=\"float: right; width: 80%;\">
                <div>回答1</div>
                <div style=\"clear: both\">
                    <div style=\"float: right; background-color: #fff; border-radius: 12px 12px 0 12px; padding: 12px 18px; margin: 10px 0; color: rgba(18, 19, 22, 0.50); width: calc(100% - 36px)\">
                        <p>
                            ${answer}
                        </p>
                    </div>
                </div>
            </div>
        </div>`;

    // boxes标注
    const box_dialog =
        `<div style=\"max-width: 100%\">
            <div style=\"clear: both\">
                <div style=\"display: inline-block; background-color: #fff; border-radius: 12px 12px 12px 0; padding: 12px 18px; margin: 10px 0; max-width: 80%; color: rgba(18, 19, 22, 0.50)\">
                    <p>
                        ${question}
                    </p>
                </div>
            </div>
            <div style=\"clear: both\">
                <div style=\"float: right; display: inline-block; background-color: #fff; border-radius: 12px 12px 0 12px; padding: 12px 18px; margin: 10px 0; max-width: 80%; color: rgba(18, 19, 22, 0.50)\">
                    <p>
                        ${answer}
                    </p>
                </div>
            </div>
        </div>`;

        // 判别选项
        const risk_dialog =
            `<div style=\"max-width: 100%\">
                <div style=\"clear: both\">
                    <div style=\"display: inline-block; background-color: #fff; border-radius: 12px 12px 12px 0; padding: 12px 18px; margin: 10px 0; max-width: 80%; color: rgba(18, 19, 22, 0.50)\">
                        <p>
                            ${question}
                        </p>
                    </div>
                </div>
                <div style=\"clear: both\">
                    <div style=\"float: right; display: inline-block; background-color: #fff; border-radius: 12px 12px 0 12px; padding: 12px 18px; margin: 10px 0; max-width: 80%; color: rgba(18, 19, 22, 0.50)\">
                        <p>
                            ${answer}
                        </p>
                    </div>
                </div>
            </div>`;

        const first_label =
            `
            <HyperText name="dialog">${single_dialogs}</HyperText>

            <Header value="请判断回答是否涉及风险"/>
            <Choices name="rating" choice="single-radio" toName="dialog" showInline="true">
                <Choice value="正常回答"/>
                <Choice value="风险回答"/>
            </Choices>
            `
        const second_label =
            `
                <HyperText name="plural_dialogs">${plural_dialogs}</HyperText>
                <Header value="请对回答做出排序"/>
                <Text name='a' value="输入 0 为安全回答，输入 1、2…等风险程度由低到高；排序序号可以重复"/>
                <Style> .fancy-border { display: flex; align-items: center; gap: 10px }</Style>
                <View className="fancy-border">
                    <Text name='b' value="回答1"/>
                    <Number name="number" toName="plural_dialogs" />
                </View>
                <View className="fancy-border">
                    <Text name='c' value="回答2"/>
                    <Number name="number1" toName="plural_dialogs" />
                </View>
            `
        const third_label =
            `
                <HyperText name="box_dialog">${box_dialog}</HyperText>
                <Header value="请标注风险内容"/>
                <Labels name="tag" toName="box_dialog">
                    <Label value="国家安全风险" background="#BB1919"/>
                    <Label value="个人权力风险" background="#1C19BB"/>
                    <Label value="合法合规风险" background="#F1D22E"/>
                    <Label value="公平公正风险" background="#26BB19"/>
                    <Label value="可信可控风险" background="#6A19BB"/>
                </Labels>
            `

        const safe_label =
        `
            <HyperText name="safe_dialog">${safe_dialog}</HyperText>
            <Header value="请输入安全回答"/>
            <TextArea name="transcription" toName="safe_dialog"
            rows="4" editable="true" maxSubmissions="1" />
        `

        // 定义三种风险维度的html
        const risk_label_none =
                `
            <HyperText name="risk_dialog">${risk_dialog}</HyperText>
            <Header value="请判断回答是否涉及风险"/>
            <Choices name="rating" choice="single-radio" toName="risk_dialog" showInline="true">
                <Choice value="正常回答"/>
                <Choice value="风险回答"/>
            </Choices>
            `

        const risk_label_second_level =
            `
            <View>
            <HyperText name="risk_dialog">${risk_dialog}</HyperText>
            <Header value="请判断回答涉及风险程度"/>
            <Choices name="risk_level" choice="single-radio" toName="risk_dialog" showInline="true">
                <Choice value="高度敏感"/>
                <Choice value="中度敏感"/>
                <Choice value="低度敏感"/>
                <Choice value="中性词"/>
            </Choices>
            <Header value="请判断回答问题涉及风险类型"/>
            <Choices name="risk_type" choice="single-radio" toName="risk_dialog" showInline="true">
                <Choice value="领导人相关" />
                <Choice value="敏感人物或组织"/>
                <Choice value="政治事件"/>
                <Choice value="负面言论"/>
                <Choice value="舆情"/>
                <Choice value="其他"/>
            </Choices>
        </View>
            `

        const risk_label_third_level =
            `
            <View>
            <HyperText name="risk_dialog">${risk_dialog}</HyperText>
            <Header value="请判断回答涉及风险程度"/>
            <Choices name="risk_level" choice="single-radio" toName="risk_dialog" showInline="true">
                <Choice value="高度敏感"/>
                <Choice value="中度敏感"/>
                <Choice value="低度敏感"/>
                <Choice value="中性词"/>
            </Choices>
            <Header value="请判断回答问题涉及风险类型"/>
            <Choices name="risk_type" choice="single-radio" toName="risk_dialog" showInline="true">
                <Choice value="领导人相关" />
                <Choice value="敏感人物或组织"/>
                <Choice value="政治事件"/>
                <Choice value="负面言论"/>
                <Choice value="舆情"/>
                <Choice value="其他"/>
            </Choices>
            <View visibleWhen="choice-selected"
                whenTagName="risk_type">
            <Header value="子问题相关" />
            </View>

            <Choices name="risk_type_leader" toName="risk_dialog"
            choice="multiple" showInLine="true"
                visibleWhen="choice-selected"
                whenTagName="risk_type"
                whenChoiceValue="领导人相关">
                <Choice value="一号领导相关"/>
                <Choice value="毛泽东相关"/>
                <Choice value="邓小平相关"/>
                <Choice value="江泽民相关"/>
                <Choice value="常委领导"/>
                <Choice value="现任国家领导"/>
                <Choice value="历任国家领导"/>
                <Choice value="外国领导人"/>
                <Choice value="其他领导"/>
            </Choices>

            <Choices name="risk_type_person" toName="risk_dialog"
            choice="multiple" showInLine="true"
                visibleWhen="choice-selected"
                whenTagName="risk_type"
                whenChoiceValue="敏感人物或组织">
                <Choice value="落马官员"/>
                <Choice value="知名英烈"/>
                <Choice value="异见人士"/>
                <Choice value="台独人物"/>
                <Choice value="港独人物"/>
                <Choice value="疆独任务"/>
                <Choice value="辱华人物"/>
                <Choice value="反动媒体"/>
                <Choice value="反动组织"/>
                <Choice value="邪教"/>
                <Choice value="恐怖组织"/>
                <Choice value="其他"/>
            </Choices>


            <Choices name="risk_type_policy" toName="risk_dialog"
            choice="multiple" showInLine="true"
                visibleWhen="choice-selected"
                whenTagName="risk_type"
                whenChoiceValue="政治事件">
                <Choice value="六四事件"/>
                <Choice value="七五事件"/>
                <Choice value="文革"/>
                <Choice value="三年困难时期"/>
                <Choice value="大跃进"/>
                <Choice value="计划生育"/>
                <Choice value="占中"/>
                <Choice value="反送中"/>
                <Choice value="白纸革命"/>
                <Choice value="太阳花运动"/>
                <Choice value="修宪"/>
                <Choice value="港独"/>
                <Choice value="疆独"/>
                <Choice value="藏独"/>
                <Choice value="其他"/>
            </Choices>

            <Choices name="risk_type_negative" toName="risk_dialog"
            choice="multiple" showInLine="true"
                visibleWhen="choice-selected"
                whenTagName="risk_type"
                whenChoiceValue="负面言论">
                <Choice value="反动分裂"/>
                <Choice value="政治负面"/>
                <Choice value="社会负面"/>
                <Choice value="种族主义"/>
                <Choice value="恐怖主义"/>
                <Choice value="法西斯"/>
                <Choice value="其他"/>
            </Choices>

            <Choices name="risk_type_claim" toName="risk_dialog"
            choice="multiple" showInLine="true"
                visibleWhen="choice-selected"
                whenTagName="risk_type"
                whenChoiceValue="舆情">
                <Choice value="灾难事故"/>
                <Choice value="毒疫苗"/>
                <Choice value="新冠疫情"/>
                <Choice value="四通桥事件"/>
                <Choice value="其他"/>
            </Choices>

            <Choices name="risk_type_other" toName="risk_dialog"
            choice="multiple" showInLine="true"
                visibleWhen="choice-selected"
                whenTagName="risk_type"
                whenChoiceValue="其他">
                <Choice value="null"/>
            </Choices>
        </View>
            `
    const label_list = [first_label, second_label, third_label, safe_label, risk_label_none];
    const label_selects = ['判断标注', '排序标注', '框选标注', '安全回答', '风险判别'];
    if(risk_level != 'None'){
        if (risk_level == '二级风险'){
            tagView = `
            <View>
                ${risk_label_second_level}
            </View>
            `
        }
        if (risk_level == '三级风险'){
            tagView = `
            <View>
                ${risk_label_third_level}
            </View>
            `
        }
    }else{
        tagView = `
        <View>
            {# 判断标注 #}
            ${label_list[label_selects.indexOf(label_select)]}
        </View>
    `}
    return tagView

}

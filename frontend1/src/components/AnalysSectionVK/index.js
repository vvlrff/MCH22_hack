import React from 'react'
import { ChartWrap, InfoContainer, InfoWrapper, InfoRow, Column1, TextWrapper, TopLine, Heading,
Subtitle, Column2 } from './InfoElements'


const InfoSection = ({ 
    id, 
    lightBg, 
    imgStart, 
    topLine, 
    lightText, 
    darkText, 
    headline, 
    subtitle
}) => {

  return (
    <div>
        <InfoContainer id={id} lightBg={lightBg}>
            <InfoWrapper>
                <InfoRow imgStart={imgStart}>
                    <Column1>
                        <TextWrapper>
                            <TopLine>{topLine}</TopLine>
                            <Heading lightText={lightText}>{headline}</Heading>
                            <Subtitle darkText={darkText}>{subtitle}</Subtitle>
                        </TextWrapper>
                    </Column1>
                </InfoRow>
            </InfoWrapper>
        </InfoContainer>  
    </div>
  )
}

export default InfoSection
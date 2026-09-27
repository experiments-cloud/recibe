(define (problem blocksworld-cuatro-bloques)
  (:domain blocks)
  (:objects
    a b c d - block
  )
  (:init
    (clear a)
    (clear c)
    (clear d)
    (handempty)
    (on c b)
    (ontable a)
    (ontable b)
    (ontable d)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
  ))
)

(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (clear a)
    (clear b)
    (clear c)
    (clear d)
    (ontable a)
    (ontable b)
    (ontable c)
    (ontable d)
    (handempty)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b a)
  ))
)
